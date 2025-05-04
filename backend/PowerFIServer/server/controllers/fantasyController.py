import logging
from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.db import get_db
from server.services.fantasyService import FantasyService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/load_league/{id}")
async def load_data(id : int, db: AsyncSession = Depends(get_db)):
    fantasyService = FantasyService()
    result = await fantasyService.get_league_data(id, db)
    if not result:
        raise HTTPException()
    return {"message": "League data loaded successfully"}