from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from PowerFIServer.server.db.db import Base


class PlayerTransactionStats(Base):

    __tablename__ = 'player_transaction_stats'

    def __init__(self, player_key):
        self.player_key = player_key
        self.total = 0
        self.add = 0
        self.drop = 0
        self.trades = 0

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_key: Mapped[str] = mapped_column(String(250), index=True)
    total: Mapped[int] = mapped_column(Integer)
    add: Mapped[int] = mapped_column(Integer)
    drop: Mapped[int] = mapped_column(Integer)
    trades: Mapped[int] = mapped_column(Integer)





