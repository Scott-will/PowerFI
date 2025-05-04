import logging

from sqlalchemy.ext.asyncio import AsyncSession

from server.StatsEngine import stats_engine
from server.YahooEngine import yahoo_engine

logger = logging.getLogger(__name__)

class FantasyService():

    async def get_league_data(self, league_id: int, db : AsyncSession) -> bool:
        try:
            await yahoo_engine.get_league_data(league_id, db)
            await stats_engine.load_stats(db)
            return True
        except Exception as e:
            logger.error("Failed to get data: ",e)
            return False