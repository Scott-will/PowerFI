from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from server.db.db import Base


class TransactionPlayers:
    addedPlayers = []
    removedPlayers = []
    addedTeam = ""
    removedTeam = ""


class Transaction(Base):

    __tablename__ = 'transactions'

    def __init__(self, transaction_id, timestamp, type, status, transactionPlayers : TransactionPlayers):
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.type = type
        self.status = status
        self.added_players = ','.join(map(str, transactionPlayers.addedPlayers)) if transactionPlayers.addedPlayers else ''
        self.removed_players = ','.join(map(str, transactionPlayers.removedPlayers)) if transactionPlayers.removedPlayers else ''
        self.team_key_added = transactionPlayers.addedTeam
        self.team_key_removed = transactionPlayers.removedTeam

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status : Mapped[str] = mapped_column(String(50))
    type : Mapped[str] = mapped_column(String(50))
    timestamp : Mapped[int] = mapped_column(Integer)
    transaction_id : Mapped[str] = mapped_column(Integer, index=True)
    added_players : Mapped[str] = mapped_column(String(100))
    removed_players : Mapped[str] = mapped_column(String(100))
    team_key_added : Mapped[str] = mapped_column(String(25))
    team_key_removed : Mapped[str] = mapped_column(String(25))


##sample transaction from yahoo
""""transaction": {
        "players": [
          {
            "player": {
              "display_position": "C",
              "editorial_team_abbr": "CLE",
              "name": {
                "ascii_first": "Jarrett",
                "ascii_last": "Allen",
                "first": "Jarrett",
                "full": "Jarrett Allen",
                "last": "Allen"
              },
              "player_id": 5835,
              "player_key": "454.p.5835",
              "position_type": "P",
              "transaction_data": {
                "destination_team_key": "454.l.51295.t.9",
                "destination_team_name": "Basket Deez Balls On Ur Face",
                "destination_type": "team",
                "source_team_key": "454.l.51295.t.11",
                "source_team_name": "The real ni**as",
                "source_type": "team",
                "type": "trade"
              }
            }
          },
          {
            "player": {
              "display_position": "PG,SG",
              "editorial_team_abbr": "CLE",
              "name": {
                "ascii_first": "Donovan",
                "ascii_last": "Mitchell",
                "first": "Donovan",
                "full": "Donovan Mitchell",
                "last": "Mitchell"
              },
              "player_id": 5826,
              "player_key": "454.p.5826",
              "position_type": "P",
              "transaction_data": {
                "destination_team_key": "454.l.51295.t.9",
                "destination_team_name": "Basket Deez Balls On Ur Face",
                "destination_type": "team",
                "source_team_key": "454.l.51295.t.11",
                "source_team_name": "The real ni**as",
                "source_type": "team",
                "type": "trade"
              }
            }
          },
          {
            "player": {
              "display_position": "SF,PF",
              "editorial_team_abbr": "ATL",
              "name": {
                "ascii_first": "Jalen",
                "ascii_last": "Johnson",
                "first": "Jalen",
                "full": "Jalen Johnson",
                "last": "Johnson"
              },
              "player_id": 6562,
              "player_key": "454.p.6562",
              "position_type": "P",
              "transaction_data": {
                "destination_team_key": "454.l.51295.t.11",
                "destination_team_name": "The real ni**as",
                "destination_type": "team",
                "source_team_key": "454.l.51295.t.9",
                "source_team_name": "Basket Deez Balls On Ur Face",
                "source_type": "team",
                "type": "trade"
              }
            }
          }
        ],
        "status": "vetoed",
        "timestamp": 1735010921,
        "tradee_team_key": "454.l.51295.t.9",
        "tradee_team_name": "Basket Deez Balls On Ur Face",
        "trader_team_key": "454.l.51295.t.11",
        "trader_team_name": "The real ni**as",
        "transaction_id": 296,
        "transaction_key": "454.l.51295.tr.296",
        "type": "trade"
      }
    }"""