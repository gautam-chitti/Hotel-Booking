from sqlalchemy.orm import Session

from src.application.interfaces.room_repository import IRoomRepository
from src.domain.entities.room import Room
from src.infrastructure.models.room_model import RoomModel


class RoomRepositoryImpl(IRoomRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_number(self, room_number: str) -> Room | None:
        room = self.session.query(RoomModel).filter_by(room_number=room_number).first()
        if not room:
            return None
        return Room(
            room_number=room.room_number,
            room_type=room.room_type
        )
    def list_all(self) -> list[Room]:
        rooms = self.session.query(RoomModel).all()
        return [
            Room(room_number=r.room_number, room_type=r.room_type)
            for r in rooms
        ]
