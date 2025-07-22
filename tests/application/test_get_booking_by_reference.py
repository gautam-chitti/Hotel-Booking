from application.use_cases.get_booking_by_reference import GetBookingByReferenceUseCase
import pytest
from uuid import uuid4
from datetime import date, timedelta

from application.use_cases.get_booking_by_reference import GetBookingByReferenceUseCase
from domain.entities.booking import Booking
from domain.entities.guest import Guest
from domain.entities.room import Room
from domain.enums import BookingStatus
from domain.value_objects.booking_reference import BookingReference
from domain.value_objects.guest_age import GuestAge
from domain.value_objects.stay_duration import StayDuration
from domain.exceptions import DomainException


def test_get_booking_by_reference_found():
    booking = Booking(
        reference=BookingReference.generate(),
        guest=Guest(uuid4(), "Test", "t@test.com", "9999999999", GuestAge(25)),
        room=Room("101", "Standard"),
        stay=StayDuration(date.today() + timedelta(days=2), date.today() + timedelta(days=4)),
        num_guests=1,
        status=BookingStatus.BOOKED,
        payment_received=True
    )

    class Repo:
        def get_by_reference(self, ref): return booking

    use_case = GetBookingByReferenceUseCase(Repo())
    result = use_case.execute(booking.reference.value)

    assert result.reference.value == booking.reference.value


def test_get_booking_by_reference_not_found():
    class Repo:
        def get_by_reference(self, ref): return None

    use_case = GetBookingByReferenceUseCase(Repo())

    with pytest.raises(DomainException):
        use_case.execute("XYZ123")
