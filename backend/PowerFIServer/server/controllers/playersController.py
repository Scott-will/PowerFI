import logging
from io import BytesIO

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from server.db.db import get_db
from server.services.playersService import PlayerService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get_players")
async def get_players(take : int,
                      skip : int,
                      order_by : str,
                      sort_asc : bool,
                      query : str = None,
                      db: AsyncSession = Depends(get_db)):
    players_service = PlayerService()
    results = await players_service.getPlayers(take, skip, order_by, sort_asc, query, db)
    return results

@router.get("/get_player/{id}")
async def get_player_by_id(id : int,
                           db: AsyncSession = Depends(get_db)):
    players_service = PlayerService()
    results = await players_service.get_player_by_id(id, db)
    return results

@router.get("/get_player_image/{id}")
async def get_player_image(id : int,
                           db : AsyncSession = Depends(get_db)):
    players_service = PlayerService()
    results = await players_service.get_player_image(id, db)
    if results.image_data is not None:
        image_stream = BytesIO(results.image_data)
        return StreamingResponse(image_stream, media_type=results.content_type)

    return None

@router.get("/get_player_transaction_stats/{player_key}")
async def get_player_transaction_stats(player_key : str, db : AsyncSession = Depends(get_db)):
    players_service = PlayerService()
    results = await players_service.get_player_transaction_stats(player_key, db)
    return results

@router.get("/get_player_transaction_stats")
async def get_player_transaction_stats(take : int,
                      skip : int,
                      order_by : str,
                      sort_asc : bool, db : AsyncSession = Depends(get_db)):
    players_service = PlayerService()
    results = await players_service.get_player_transaction_stats_paginated(take, skip, order_by, sort_asc, db)
    return results