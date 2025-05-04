import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PowerFIServer.server.controllers import fantasyController, playersController, transactionsController, fantasyTeamsController

logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Starting up fast api server')


app = FastAPI()

logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Starting up fast api server')

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(fantasyController.router, prefix="/api/fantasy", tags=["fantasy"])
app.include_router(playersController.router, prefix="/api/players", tags=["players"])
app.include_router(fantasyTeamsController.router, prefix="/api/teams", tags=["teams"])
app.include_router(transactionsController.router, prefix="/api/transactions", tags=["transactions"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
