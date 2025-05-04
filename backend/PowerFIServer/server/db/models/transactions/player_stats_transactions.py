from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from PowerFIServer.server.db.db import Base


class PlayerStatsByTransaction(Base):

    __tablename__ = 'player_stats_by_transaction'

    def __init__(self, player_id, transaction_id, fantasy_points):
        self.player_id = player_id
        self.transaction_id = transaction_id
        self.fantasy_points = fantasy_points

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(50))
    fantasy_points: Mapped[str] = mapped_column(String(50))