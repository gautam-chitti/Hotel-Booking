from application.use_cases.check_room_availability import CheckRoomAvailabilityUseCase
from datetime import date, timedelta
from application.use_cases.check_room_availability import CheckRoomAvailabilityUseCase


def test_check_room_availability_filters_unavailable():
    class Room:
        def __init__(self, room_number): self.room_number = room_number; self.room_type = "Standard"
        @property
        def capacity(self): return 2
        @property
        def price_per_night(self): return 100

    class RoomRepo:
        def list_all(self): return [Room("101"), Room("102")]

    class BookingRepo:
        def is_room_available(self, room_number, check_in, check_out):
            return room_number == "102"

    use_case = CheckRoomAvailabilityUseCase(RoomRepo(), BookingRepo())
    result = use_case.execute(date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    assert len(result) == 1
    assert result[0].room_number == "102"
