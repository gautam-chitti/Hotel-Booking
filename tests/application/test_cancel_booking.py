import pytest
from datetime import date, timedelta
from domain.entities.booking import Booking
from domain.entities.guest import Guest
from domain.entities.room import Room
from domain.enums import BookingStatus
from domain.value_objects.guest_age import GuestAge
from domain.value_objects.booking_reference import BookingReference
from domain.value_objects.stay_duration import StayDuration
from application.use_cases.cancel_booking import CancelBookingUseCase
from domain.exceptions import DomainException
from uuid import uuid4


class FakeBookingRepo:
    def __init__(self, booking):
        self.booking = booking
        self.updated = False

    def get_by_reference(self, ref):
        return self.booking

    def update(self, booking):
        self.updated = True


def test_cancel_booking_success():
    guest = Guest(uuid4(), "Test", "t@test.com", "9999999999", GuestAge(25))
    room = Room("101", "Standard")
    stay = StayDuration(
        date.today() + timedelta(days=3),
        date.today() + timedelta(days=5)
    )
    booking = Booking(
        reference=BookingReference.generate(),
        guest=guest,
        room=room,
        stay=stay,
        num_guests=1,
        status=BookingStatus.BOOKED,
        payment_received=True
    )
    repo = FakeBookingRepo(booking)
    use_case = CancelBookingUseCase(repo)

    use_case.execute(booking.reference.value)
    assert booking.status == BookingStatus.CANCELLED
    assert repo.updated is True


def test_cancel_booking_too_late():
    guest = Guest(uuid4(), "Test", "t@test.com", "9999999999", GuestAge(25))

    room = Room("101", "Standard")
    stay = StayDuration(
        date.today() + timedelta(days=1),
        date.today() + timedelta(days=3)
    )
    booking = Booking(
        reference=BookingReference.generate(),
        guest=guest,
        room=room,
        stay=stay,
        num_guests=1,
        status=BookingStatus.BOOKED,
        payment_received=True
    )
    repo = FakeBookingRepo(booking)
    use_case = CancelBookingUseCase(repo)

    with pytest.raises(DomainException):
        use_case.execute(booking.reference.value)
