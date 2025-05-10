from pydantic.v1 import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from PowerFIServer.server.db.db import Base


class FantasyTeam(Base):

    __tablename__ = 'fantasy_teams'

    def __init__(self, team_id, name, manager_name, team_key):
        self.team_id = team_id
        self.name = name
        self.manager_name = manager_name
        self.team_key = team_key

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, index=True)
    team_key: Mapped[str] = mapped_column(String(25), index=True)
    name: Mapped[str] = mapped_column(String(250))
    manager_name: Mapped[str] = mapped_column(String(250))
    picture : Mapped[int] = mapped_column(Integer, nullable=True)
    picture_url : Mapped[str] = mapped_column(String(250))

    pictures = relationship("FantasyTeamImage", back_populates="fantasy_team")



##sample team from yahoo
""""team": {
        "has_draft_grade": 0,
        "league_scoring_type": "headpoint",
        "managers": {
          "manager": {
            "email": "koobie1324@gmail.com",
            "felo_score": 649,
            "felo_tier": "silver",
            "guid": "CSVFF47LM6MVNFGBGEKPI2KAMY",
            "image_url": "https://s.yimg.com/ag/images/6df4079e-5f56-4148-bd59-d3463de8c658hb_64sq.jpg",
            "is_commissioner": 0,
            "manager_id": 1,
            "nickname": "Jacob"
          }
        },
        "name": "Islamic state of nosketball",
        "number_of_moves": 19,
        "number_of_trades": 2,
        "roster_adds": {
          "coverage_type": "week",
          "coverage_value": 9,
          "value": 0
        },
        "team_id": 1,
        "team_key": "454.l.51295.t.1",
        "team_logos": {
          "team_logo": {
            "size": "large",
            "url": "https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/3e747dcfe6b72f273aa78ac0650f4275fdfe660db98d7662dfd0de0d022cc989.jpg"
          }
        },
        "url": "https://basketball.fantasysports.yahoo.com/nba/51295/1",
        "waiver_priority": 3
      }
    }"""