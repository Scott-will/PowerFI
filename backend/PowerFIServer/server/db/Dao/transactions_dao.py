from sqlalchemy import select, func, or_
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from PowerFIServer.server.db.models.players.player import Player
from PowerFIServer.server.db.models.teams.fantasy_team import FantasyTeam
from PowerFIServer.server.db.models.transactions.player_stats_transactions import PlayerStatsByTransaction
from PowerFIServer.server.db.models.transactions.transaction import Transaction

logger = logging.getLogger(__name__)

async def save_transactions(transactions: [Transaction], db : AsyncSession):
    try:
        existing_transactions = await db.execute(select(Transaction))
        existing_transactions = existing_transactions.scalars().all()
        existing_transactions_map = {t.transaction_id: t for t in existing_transactions}
        for transaction in transactions:
            if transaction.transaction_id in existing_transactions_map:
                existing_transaction = existing_transactions_map[transaction.transaction_id]
                existing_transaction.status = transaction.status
                existing_transaction.type = transaction.type
                existing_transaction.timestamp = transaction.timestamp
                existing_transaction.teamKeyRemoved = transaction.teamKeyRemoved
                existing_transaction.teamKeyAdded = transaction.teamKeyAdded
                existing_transaction.removedPlayers = transaction.removedPlayers
                existing_transaction.addedPlayers = transaction.addedPlayers
            else:
                db.add(transaction)

        await db.commit()
    except Exception as e:
        logger.error(f"Error saving transactions: {e}")

async def get_transactions(take : int, skip : int, player : str, team : str, type : str, db : AsyncSession) -> [Transaction]:

    total_result = await db.execute(select(func.count(Transaction.id)))
    total = total_result.scalar()
    query = select(Transaction).limit(take).offset(skip)
    if player:
        player_subquery = (
            select(Player.player_id)
            .where(
                or_(
                    Player.first_name.ilike(f"%{player}%"),
                    Player.last_name.ilike(f"%{player}%")
                )
            )
        )

        matching_player_ids = (await db.execute(player_subquery)).scalars().all()

        if matching_player_ids:
            matching_player_ids = [str(pid) for pid in matching_player_ids]

            player_conditions = [
                or_(
                    Transaction.added_players.ilike(f'%{pid}%'),
                    Transaction.removed_players.ilike(f'%{pid}%'),
                )
                for pid in matching_player_ids
            ]
            query = query.where(or_(*player_conditions))
        else:
            return {
                "total": 0,
                "items": []
            }
    if team:
        team_subquery = (
            select(FantasyTeam.team_key)
            .where(
                FantasyTeam.name.ilike(f"%{team}%")
            )
        )
        matching_team_keys = (await db.execute(team_subquery)).scalars().all()

        if matching_team_keys:
            matching_team_keys = [str(tk) for tk in matching_team_keys]
            team_conditions = [
                or_(
                    Transaction.team_key_added.ilike(f'%{tk}%'),
                    Transaction.team_key_removed.ilike(f'%{tk}%'),
                )
                for tk in matching_team_keys
            ]
            query = query.where(or_(*team_conditions))
    if type:
        if type != "all":
            query = query.where(Transaction.type == type)
    results = await db.execute(query)
    transactions = results.scalars().all()
    return {
        "total": total,
        "items": transactions
    }

async def get_trades(take : int, skip : int, db : AsyncSession) -> [Transaction]:
    total_result = await db.execute(select(func.count(Transaction.id)).select_from(select(Transaction)))
    total = total_result.scalar()
    results = await db.execute(select(Transaction).filter(Transaction.type == 'trade').limit(take).offset(skip))
    transactions = results.scalars().all()
    return {
        "total": total,
        "items": transactions
    }

async def get_waivers(take : int, skip : int, db : AsyncSession) -> [Transaction]:
    total_result = await db.execute(select(func.count(Transaction.id)).select_from(select(Transaction)))
    total = total_result.scalar()
    results = await db.execute(select(Transaction).filter(Transaction.type != 'trade').limit(take).offset(skip))
    transactions = results.scalars().all()
    return {
        "total": total,
        "items": transactions
    }

async def get_transactions_for_player(player_id : str, db : AsyncSession) -> [Transaction]:
    stmt = select(Transaction).filter(
        (Transaction.added_players.like(f"%{player_id}%")) |
        (Transaction.removed_players.like(f"%{player_id}%"))
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()
    return transactions

async def get_transactions_for_team(team_key : str, db : AsyncSession) -> [Transaction]:
    stmt = select(Transaction).filter(
        (Transaction.team_key_added.like(f"%{team_key}%")) |
        (Transaction.team_key_removed.like(f"%{team_key}%"))
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()
    return transactions

async def get_related_transactions(transaction_id : str, db : AsyncSession) -> [Transaction]:
    query = select(Transaction).filter(Transaction.transaction_id == transaction_id)
    transaction_look_up = await db.execute(query)
    transaction = transaction_look_up.scalars().all()[0]
    if transaction is None:
        logger.error("Failed to find transaction with id: ", transaction_id)
        return []

    player_filter = []
    players = list(set(transaction.added_players.split(",") + transaction.removed_players.split(",")))
    for p in players:
        p = p.strip()
        if not p:
            continue
        player_filter.append(Transaction.added_players.like(f"%{p}%"))
        player_filter.append(Transaction.removed_players.like(f"%{p}%"))
    if player_filter.count == 0:
        return []
    query = select(Transaction).filter(or_(*player_filter)).filter(Transaction.timestamp >= transaction.timestamp).order_by(Transaction.timestamp)
    results = await db.execute(query)
    transactions = results.scalars().all()
    return transactions

async def get_transaction_stats(transaction_id : str, db : AsyncSession) -> [PlayerStatsByTransaction]:
    query = select(PlayerStatsByTransaction).filter(PlayerStatsByTransaction.transaction_id == transaction_id)
    transactions = await db.execute(query)
    stats = transactions.scalars().all()
    return stats

async def get_player_transaction_stats(player_id : str, db : AsyncSession) -> [PlayerStatsByTransaction]:
    transactions = await get_transactions_for_player(player_id, db)
    transaction_ids = [transaction.transaction_id for transaction in transactions]
    query = select(PlayerStatsByTransaction).filter(
        PlayerStatsByTransaction.transaction_id.in_(transaction_ids))
    stats = await db.execute(query)
    stats = stats.scalars().all()
    return stats
