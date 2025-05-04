from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.models.players.player import Player
from PowerFIServer.server.db.models.players.player_transaction_stats import PlayerTransactionStats
from PowerFIServer.server.db.models.teams.fantasy_team import FantasyTeam
from PowerFIServer.server.db.models.teams.fantasy_team_transaction_stats import FantasyTeamTransactionStats
from PowerFIServer.server.db.models.transactions.transaction import Transaction


class StatsEngine:

    async def load_stats(self, db : AsyncSession):
        await self.LoadTeamTransactionStats(db)
        await self.LoadPlayerTransactionStats(db)

    async def LoadPlayerTransactionStats(self, db : AsyncSession):
        result = await db.execute(select(Player))
        players = result.scalars().all()
        for player in players:
            item = PlayerTransactionStats(player.player_key)
            result = await db.execute(
                select(Transaction).filter(
                    or_(
                        Transaction.added_players.contains(player.player_id),
                        Transaction.removed_players.contains(player.player_id)
                    )
                )
            )
            transactions = result.scalars().all()
            item.total = len(transactions)
            item.trades = sum(1 for t in transactions if t.type == "trade")
            item.add = sum(1 for t in transactions if t.type == "add" or t.type == "add/drop")
            item.drop = sum(1 for t in transactions if t.type == "drop" or t.type == "add/drop")
            db.add(item)
        await db.commit()

    async def LoadTeamTransactionStats(self, db : AsyncSession):
        result = await db.execute(select(FantasyTeam))
        teams = result.scalars().all()
        for team in teams:
            item = FantasyTeamTransactionStats(team.team_key)
            result = await db.execute(
                select(Transaction).filter(
                    or_(
                        Transaction.team_key_added.contains(team.team_key),
                        Transaction.team_key_removed.contains(team.team_key)
                    )
                )
            )
            transactions = result.scalars().all()
            item.total = len(transactions)
            item.trades = sum(1 for t in transactions if t.type == "trade")
            item.add = sum(1 for t in transactions if t.type == "add" or t.type == "add/drop")
            item.drop = sum(1 for t in transactions if t.type == "drop" or t.type == "add/drop")
            db.add(item)
        await db.commit()

stats_engine = StatsEngine()