from enum import Enum


class BookingStatus(Enum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"
    CHECKED_IN = "CheckedIn"
    CHECKED_OUT = "CheckedOut"
