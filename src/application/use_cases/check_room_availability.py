from datetime import date

from src.application.interfaces.booking_repository import IBookingRepository
from src.application.interfaces.room_repository import IRoomRepository
from src.domain.entities.room import Room


class CheckRoomAvailabilityUseCase:
    def __init__(self, room_repo: IRoomRepository, booking_repo: IBookingRepository):
        self.room_repo = room_repo
        self.booking_repo = booking_repo

    def execute(self, check_in: date, check_out: date) -> list[Room]:
        available_rooms = []
        for room in self.room_repo.list_all():
            if self.booking_repo.is_room_available(room.room_number, check_in, check_out):
                available_rooms.append(room)
        return available_rooms
