from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, foreign, relationship

from PowerFIServer.server.db.db import Base


class FantasyTeamImage(Base):
    __tablename__ = 'fantasy_team_image'

    def __init__(self, fantasy_team_id, image_data, content_type):
        self.fantasy_team_id = fantasy_team_id
        self.image_data = image_data
        self.content_type = content_type

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fantasy_team_id : Mapped[int] = mapped_column(Integer, ForeignKey("fantasy_teams.id"))
    image_data : Mapped[bytes] = mapped_column(BYTEA)
    content_type : Mapped[str] = mapped_column(String(250))

    fantasy_team = relationship("FantasyTeam", back_populates="pictures")
