import logging

from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.Dao import players_dao
from PowerFIServer.server.db.models.players.player import Player
from PowerFIServer.server.db.models.players.player_image import PlayerImage
from PowerFIServer.server.db.models.players.player_transaction_stats import PlayerTransactionStats

logger = logging.getLogger(__name__)

class PlayerService:
    #paginated api to get players
    async def getPlayers(self, take : int,
                         skip : int,
                         order_by : str,
                         sort_asc : bool,
                         query : str,
                         db : AsyncSession):
        try:
            return await players_dao.get_players(take, skip, order_by, sort_asc, query, db)
        except Exception as e:
            logger.error("Failed to get players", e)
            return []

    async def get_player_by_id(self, id : int, db : AsyncSession) -> Player | None:
        try:
            return await players_dao.get_player_by_id(id, db)
        except Exception as e:
            logger.error("Failed to get players", e)
            return None

    async def get_player_image(self, id : int, db : AsyncSession) -> PlayerImage | None:
        try:
            return await players_dao.get_player_image(id, db)
        except Exception as e:
            logger.error("Failed to get players", e)
            return None

    async def get_player_transaction_stats(self, player_key : str, db : AsyncSession) -> [PlayerTransactionStats]:
        try:
            return await players_dao.get_player_transaction_stats(player_key, db)
        except Exception as e:
            logger.error("Failed to get player transaction stats", e)
            return None

    async def get_player_transaction_stats_paginated(self, take : int, skip : int, order_by : str, sort_asc : bool, db : AsyncSession) -> [PlayerTransactionStats]:
        try:
            return await players_dao.get_player_transaction_stats_paginated(take, skip, order_by, sort_asc, db)
        except Exception as e:
            logger.error("Failed to get player transaction stats", e)
            return None
