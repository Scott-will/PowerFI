from io import BytesIO
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from server.db.db import get_db
from server.services.fantasyTeamsService import FantasyTeamsService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get_fantasy_teams")
async def get_fantasy_teams(take : int, skip : int,  db: AsyncSession = Depends(get_db)):
    fantasy_teams_service = FantasyTeamsService()
    return await fantasy_teams_service.getFantasyTeams(take, skip, db)

@router.get("/get_team_image/{id}")
async def get_player_image(id : int,
                           db : AsyncSession = Depends(get_db)):
    fantasy_teams_service = FantasyTeamsService()
    results = await fantasy_teams_service.get_fantasy_team_image(id, db)
    if results.image_data is not None:
        # Send the image as a file response
        image_stream = BytesIO(results.image_data)
        return StreamingResponse(image_stream, media_type=results.content_type)

@router.get("/get_team_transaction_stats")
async def get_team_transaction_stats(team_key : str, db : AsyncSession = Depends(get_db)):
    fantasy_teams_service = FantasyTeamsService()
    results = await fantasy_teams_service.get_team_transaction_stats(team_key, db)
    return results

@router.get("/get_all_team_transaction_stats")
async def get_all_team_transaction_stats(order_by : str, sort_asc : bool, db : AsyncSession = Depends(get_db)):
    fantasy_teams_service = FantasyTeamsService()
    results = await fantasy_teams_service.get_all_team_transaction_stats(order_by, sort_asc, db)
    return results
