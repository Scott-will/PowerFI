import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.db import get_db
from PowerFIServer.server.services.transactionsService import TransactionsService

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/get_transactions")
async def get_transactions(take : int, skip : int,  player : str = None, type : str = None, db: AsyncSession = Depends(get_db)):
    transactions_service = TransactionsService()
    return await transactions_service.getTransactions(take, skip, player, type, db)

@router.get("/get_trades")
async def get_trades(take : int, skip : int, db: AsyncSession = Depends(get_db)):
    transactions_service = TransactionsService()
    return await transactions_service.getTrades(take, skip, db)

@router.get("/get_waiver")
async def get_waivers(take : int, skip : int, db: AsyncSession = Depends(get_db)):
    transactions_service = TransactionsService()
    return await transactions_service.get_waivers(take, skip, db)

@router.get("/player_transactions")
async def get_transactions_for_player(player : str, db : AsyncSession = Depends(get_db)):
    transactions_service = TransactionsService()
    return await transactions_service.get_transactions_for_players(player, db)

@router.get("/team_transactions")
async def get_transactions_for_player(team_key : str, db : AsyncSession = Depends(get_db)):
    transactions_service = TransactionsService()
    return await transactions_service.get_transactions_for_teams(team_key, db)

@router.get("/related_transactions")
async def get_related_transactions(transaction_id : str, db : AsyncSession = Depends(get_db)):
    transactions_service = TransactionsService()
    return await transactions_service.get_related_transactions(transaction_id, db)

@router.get("/transaction_stats")
async def get_transaction_stats(transaction_id : str, db : AsyncSession = Depends(get_db)):
    transaction_service = TransactionsService()
    return await transaction_service.get_transaction_stats(transaction_id, db)

@router.get("/player_transaction_stats")
async def get_player_transaction_stats(transaction_id : str, db : AsyncSession = Depends(get_db)):
    transaction_service = TransactionsService()
    return await transaction_service.get_player_transaction_stats(transaction_id, db)