import logging

from sqlalchemy.ext.asyncio import AsyncSession

from server.db.Dao.fantasy_team_dao import get_fantasy_teams, get_team_image, get_team_transaction_stats, \
    get_all_team_transaction_stats
from server.db.models.teams.fantasy_team import FantasyTeam
from server.db.models.teams.fantasy_team_image import FantasyTeamImage
from server.db.models.teams.fantasy_team_transaction_stats import FantasyTeamTransactionStats

logger = logging.getLogger(__name__)

class FantasyTeamsService:
    #paginated api to get players
    async def getFantasyTeams(self, take : int, skip : int, db : AsyncSession) -> [FantasyTeam]:
        try:
            return await get_fantasy_teams(take, skip, db)
        except:
            ##log
            return []

    async def get_fantasy_team_image(self, id : int, db : AsyncSession) -> FantasyTeamImage | None:
        try:
            return await get_team_image(id, db)
        except:
            return None

    async def get_team_transaction_stats(self, team_key : str, db : AsyncSession) -> [FantasyTeamTransactionStats]:
        try:
            return await get_team_transaction_stats(team_key, db)
        except:
            return None

    async def get_all_team_transaction_stats(self, order_by : str, sort_asc : bool, db : AsyncSession) -> [FantasyTeamTransactionStats]:
        try:
            return await get_all_team_transaction_stats(order_by, sort_asc, db)
        except:
            return None