from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.base import Base


class RoomModel(Base):
    __tablename__ = "rooms"

    room_number: Mapped[str] = mapped_column(String, primary_key=True)
    room_type: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_night: Mapped[int] = mapped_column(Integer, nullable=False)
