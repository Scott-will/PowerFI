from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, foreign, relationship

from PowerFIServer.server.db.db import Base


class PlayerImage(Base):
    __tablename__ = 'player_images'

    def __init__(self, player_id, image_data, content_type):
        self.player_id = player_id
        self.image_data = image_data
        self.content_type = content_type

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id : Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    image_data : Mapped[bytes] = mapped_column(BYTEA)
    content_type : Mapped[str] = mapped_column(String(250))

    player = relationship("Player", back_populates="pictures")


