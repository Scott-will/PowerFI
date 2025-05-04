from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from server.db.db import Base


class FantasyTeamTransactionStats(Base):
    __tablename__ = 'fantasy_team_transaction_stats'

    def __init__(self, team_key : str):
        self.team_key = team_key
        self.total = 0
        self.add = 0
        self.drop = 0
        self.trades = 0

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_key: Mapped[str] = mapped_column(String(250), index=True)
    total: Mapped[int] = mapped_column(Integer)
    add: Mapped[int] = mapped_column(Integer)
    drop: Mapped[int] = mapped_column(Integer)
    trades: Mapped[int] = mapped_column(Integer)