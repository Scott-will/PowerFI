import logging

from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.models.teams.fantasy_team import FantasyTeam
from PowerFIServer.server.db.models.teams.fantasy_team_image import FantasyTeamImage
from PowerFIServer.server.db.models.teams.fantasy_team_transaction_stats import FantasyTeamTransactionStats

logger = logging.getLogger(__name__)

async def save_fantasy_teams(teams: [FantasyTeam], db : AsyncSession):
    try:
        existing_teams = await db.execute(select(FantasyTeam))
        existing_teams = existing_teams.scalars().all()
        existing_teams_map = {t.team_id: t for t in existing_teams}
        for team in teams:
            if team.team_id in existing_teams_map:
                existing_team = existing_teams_map[team.team_id]
                existing_team.name = team.name
                existing_team.position = team.position
                existing_team.manager_name = team.manager_name
            else:
                db.add(team)
        await db.commit()
    except Exception as e:
        logger.error(f"Error saving teams: {e}")



async def get_fantasy_teams(take : int, skip : int, db : AsyncSession) -> [FantasyTeam]:
    results = await db.execute(select(FantasyTeam).limit(take).offset(skip))
    return results.scalars().all()

async def get_team_transaction_stats(team_key : str, db : AsyncSession) -> [FantasyTeamTransactionStats]:
    results = await db.execute(select(FantasyTeamTransactionStats).where(FantasyTeamTransactionStats.team_key == team_key))
    return results.scalars().all()

async def get_all_team_transaction_stats(order_by : str, sort_asc : bool, db : AsyncSession) -> [FantasyTeamTransactionStats]:
    base_query = select(FantasyTeamTransactionStats)
    if sort_asc:
        base_query = base_query.order_by(asc(getattr(FantasyTeamTransactionStats, order_by)))
    else:
        base_query = base_query.order_by(desc(getattr(FantasyTeamTransactionStats, order_by)))
    results = await db.execute(base_query)
    return results.scalars().all()