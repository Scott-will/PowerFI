from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.models.players.player_image import PlayerImage


async def get_player_image(id : int, db : AsyncSession) -> PlayerImage:
    results = await db.execute(select(PlayerImage).where(PlayerImage.id == id))
    return results.scalars().first()
