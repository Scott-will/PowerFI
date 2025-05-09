from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.models.teams.fantasy_team_image import FantasyTeamImage


async def get_team_image(id : int, db : AsyncSession) -> FantasyTeamImage:
    results = await db.execute(select(FantasyTeamImage).where(FantasyTeamImage.id == id))
    return results.scalars().first()