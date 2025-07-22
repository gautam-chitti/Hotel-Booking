from dataclasses import dataclass, field
from datetime import date

from src.domain.entities.guest import Guest
from src.domain.entities.room import Room
from src.domain.enums import BookingStatus
from src.domain.exceptions import DomainException
from src.domain.value_objects.booking_reference import BookingReference
from src.domain.value_objects.stay_duration import StayDuration


@dataclass
class Booking:
    reference: BookingReference
    guest: Guest
    room: Room
    stay: StayDuration
    num_guests: int
    status: BookingStatus = field(default=BookingStatus.BOOKED)
    payment_received: bool = field(default=False)

    def __post_init__(self):
        if self.num_guests > self.room.capacity:
            raise DomainException(
                f"{self.room.room_type} rooms can only hold up to {self.room.capacity} guest(s)."
            )
        if not self.payment_received:
            raise DomainException("Payment must be received at time of booking.")

    def cancel(self, today: date):
        """Allow free cancellation only if 48+ hours before check-in"""
        delta = (self.stay.check_in - today).days
        if delta < 2:
            raise DomainException("Cannot cancel less than 48 hours before check-in.")
        self.status = BookingStatus.CANCELLED

    def check_in(self):
        if self.status != BookingStatus.BOOKED:
            raise DomainException("Only booked reservations can be checked in.")
        self.status = BookingStatus.CHECKED_IN

    def check_out(self):
        if self.status != BookingStatus.CHECKED_IN:
            raise DomainException("Guest must be checked in before checking out.")
        self.status = BookingStatus.CHECKED_OUT
