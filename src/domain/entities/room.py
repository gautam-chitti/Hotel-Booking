from dataclasses import dataclass
from typing import Literal

from src.domain.exceptions import DomainException

# Allowed room types and their constraints
ROOM_TYPE_DETAILS = {
    "Standard": {"capacity": 2, "price": 100},
    "Deluxe": {"capacity": 3, "price": 200},
    "Suite": {"capacity": 4, "price": 300},
}


@dataclass(frozen=True)
class Room:
    room_number: str
    room_type: Literal["Standard", "Deluxe", "Suite"]

    def __post_init__(self):
        if self.room_type not in ROOM_TYPE_DETAILS:
            raise DomainException(f"Invalid room type: {self.room_type}")
        
        if not self.room_number or not self.room_number.isdigit() or len(self.room_number) != 3:
            raise DomainException("Room number must be a 3-digit string like '301'.")

    @property
    def capacity(self) -> int:
        return ROOM_TYPE_DETAILS[self.room_type]["capacity"]

    @property
    def price_per_night(self) -> int:
        return ROOM_TYPE_DETAILS[self.room_type]["price"]
