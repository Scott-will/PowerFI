from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from server.db.db import Base


class Player(Base):

    __tablename__ = 'players'

    def __init__(self, player_id, player_key, first_name, last_name, position, team):
        self.player_id = player_id
        self.player_key = player_key
        self.position = position
        self.first_name = first_name
        self.last_name = last_name
        self.team = team

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position : Mapped[str] = mapped_column(String(50))
    team: Mapped[str] = mapped_column(String(50))
    first_name : Mapped[str] = mapped_column(String(50))
    last_name : Mapped[str] = mapped_column(String(50))
    player_id : Mapped[int] = mapped_column(Integer, index=True)
    player_key: Mapped[str] = mapped_column(String(250), index=True)
    picture : Mapped[int] = mapped_column(Integer, nullable=True)
    picture_url : Mapped[str] = mapped_column(String(250))

    pictures = relationship("PlayerImage", back_populates="player")

##sample player object from yahoo
"""
"player": {
        "display_position": "SF,PF",
        "editorial_player_key": "nba.p.3704",
        "editorial_team_abbr": "LAL",
        "editorial_team_full_name": "Los Angeles Lakers",
        "editorial_team_key": "nba.t.13",
        "editorial_team_url": "https://sports.yahoo.com/nba/teams/la-lakers/",
        "eligible_positions": [
          "SF"
        ],
        "eligible_positions_to_add": [
          {
            "position": "PG"
          },
          {
            "position": "G"
          },
          {
            "position": "SG"
          },
          {
            "position": "F"
          },
          {
            "position": "C"
          }
        ],
        "has_player_notes": 1,
        "headshot": {
          "size": "small",
          "url": "https://s.yimg.com/iu/api/res/1.2/d0ar3r622Gyr2j8MzXacTQ--~C/YXBwaWQ9eXNwb3J0cztjaD0yMzM2O2NyPTE7Y3c9MTc5MDtkeD04NTc7ZHk9MDtmaT11bGNyb3A7aD02MDtxPTEwMDt3PTQ2/https://s.yimg.com/xe/i/us/sp/v/nba_cutout/players_l/10292024/3704.png"
        },
        "image_url": "https://s.yimg.com/iu/api/res/1.2/d0ar3r622Gyr2j8MzXacTQ--~C/YXBwaWQ9eXNwb3J0cztjaD0yMzM2O2NyPTE7Y3c9MTc5MDtkeD04NTc7ZHk9MDtmaT11bGNyb3A7aD02MDtxPTEwMDt3PTQ2/https://s.yimg.com/xe/i/us/sp/v/nba_cutout/players_l/10292024/3704.png",
        "injury_note": "Foot",
        "is_keeper": {
          "status": false,
          "cost": false,
          "kept": false
        },
        "is_undroppable": 1,
        "name": {
          "ascii_first": "LeBron",
          "ascii_last": "James",
          "first": "LeBron",
          "full": "LeBron James",
          "last": "James"
        },
        "player_id": 3704,
        "player_key": "454.p.3704",
        "player_notes_last_timestamp": 1734913286,
        "position_type": "P",
        "primary_position": "SF",
        "status": "GTD",
        "status_full": "Game Time Decision",
        "uniform_number": 23,
        "url": "https://sports.yahoo.com/nba/players/3704"
      }
      """