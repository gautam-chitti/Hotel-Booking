from dataclasses import dataclass
from datetime import date


@dataclass
class CreateBookingDTO:
    guest_id: str
    room_number: str
    num_guests: int
    check_in: date
    check_out: date
