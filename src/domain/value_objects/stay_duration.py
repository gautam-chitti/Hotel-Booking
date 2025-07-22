from dataclasses import dataclass
from datetime import date, timedelta

from src.domain.exceptions import DomainException


@dataclass(frozen=True)
class StayDuration:
    check_in: date
    check_out: date

    def __post_init__(self):
        if self.check_in < date.today() + timedelta(days=1):
            raise DomainException("Bookings must be made at least 24 hours in advance.")
        if self.check_out <= self.check_in:
            raise DomainException("Check-out date must be after check-in date.")
        if (self.check_out - self.check_in).days > 30:
            raise DomainException("Booking cannot exceed 30 nights.")
