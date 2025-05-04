import logging

from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from PowerFIServer.server.db.models.players.player import Player
from PowerFIServer.server.db.models.players.player_image import PlayerImage
from PowerFIServer.server.db.models.players.player_transaction_stats import PlayerTransactionStats

logger = logging.getLogger(__name__)

async def save_players(players: [Player], db : AsyncSession):
    try:
        existing_players = await db.execute(select(Player))
        existing_players = existing_players.scalars().all()
        existing_players_map = {t.player_id: t for t in existing_players}
        for player in players:
            if player.player_id in existing_players_map:
                existing_player = existing_players_map[player.player_id]
                existing_player.first_name = player.first_name
                existing_player.last_name = player.last_name
                existing_player.team = player.team
                existing_player.position = player.position
            else:
                db.add(player)
        await db.commit()
    except Exception as e:
        logger.error(f"Error saving players: {e}")


async def get_players(take : int,
                      skip : int,
                      order_by : str,
                      sort_asc : bool,
                      query : str,
                      db : AsyncSession) -> [Player]:
    base_query = select(Player)
    if query:
        try:
            property, value = query.split('=')
            property = property.strip()
            value = value.strip()

            filter_condition = getattr(Player, property).ilike(f"%{value}%")
            base_query = base_query.where(filter_condition)
        except ValueError:
            raise ValueError("Query should be in 'property=value' format")

    total_result = await db.execute(select(func.count(Player.id)))
    total = total_result.scalar()
    if sort_asc:
        base_query = base_query.order_by(asc(getattr(Player, order_by)))
    else:
        base_query = base_query.order_by(desc(getattr(Player, order_by)))

    base_query = base_query.limit(take).offset(skip)

    results = await db.execute(base_query)
    players = results.scalars().all()

    return {
    "total": total,
    "items": players
    }

async def get_player_by_id(id : int, db : AsyncSession) -> Player:
    results = await db.execute(select(Player).where(Player.id == id))
    return results.scalars().first()

async def get_player_image(id : int, db : AsyncSession) -> PlayerImage:
    results = await db.execute(select(PlayerImage).where(PlayerImage.id == id))
    return results.scalars().first()

async def get_player_transaction_stats(player_key : str, db : AsyncSession) -> [PlayerTransactionStats]:
    results = await db.execute(select(PlayerTransactionStats).where(PlayerTransactionStats.player_key == player_key))
    return results.scalars().all()

async def get_player_transaction_stats_paginated(take : int,
                      skip : int,
                      order_by : str,
                      sort_asc : bool,
                                                 db : AsyncSession) -> [PlayerTransactionStats]:
    base_query = select(PlayerTransactionStats)

    total_result = await db.execute(select(func.count(PlayerTransactionStats.id)))
    total = total_result.scalar()
    if sort_asc:
        base_query = base_query.order_by(asc(getattr(PlayerTransactionStats, order_by)))
    else:
        base_query = base_query.order_by(desc(getattr(PlayerTransactionStats, order_by)))

    base_query = base_query.limit(take).offset(skip)

    results = await db.execute(base_query)
    players = results.scalars().all()

    return {
        "total": total,
        "items": players
    }