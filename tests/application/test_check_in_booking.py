from application.use_cases.check_in_booking import CheckInBookingUseCase
from domain.entities.booking import Booking
from domain.entities.room import Room
from domain.entities.guest import Guest
from domain.enums import BookingStatus
from domain.value_objects.booking_reference import BookingReference
from domain.value_objects.stay_duration import StayDuration
from domain.value_objects.guest_age import GuestAge
from domain.exceptions import DomainException
from datetime import date, timedelta
from uuid import uuid4


class FakeRepo:
    def __init__(self, booking):
        self.booking = booking
        self.updated = False

    def get_by_reference(self, ref):
        return self.booking

    def update(self, booking):
        self.updated = True


def test_check_in_success():
    booking = Booking(
        reference=BookingReference.generate(),
        guest=Guest(uuid4(), "Test", "t@test.com", "9999999999", GuestAge(25)),
        room=Room("101", "Standard"),
        stay=StayDuration(date.today() + timedelta(days=2), date.today() + timedelta(days=4)),
        num_guests=1,
        status=BookingStatus.BOOKED,
        payment_received=True
    )
    repo = FakeRepo(booking)
    use_case = CheckInBookingUseCase(repo)

    use_case.execute(booking.reference.value)
    assert booking.status == BookingStatus.CHECKED_IN
    assert repo.updated


def test_check_in_invalid_status():
    booking = Booking(
        reference=BookingReference.generate(),
        guest=Guest(uuid4(), "Test", "t@test.com", "9999999999", GuestAge(25)),
        room=Room("101", "Standard"),
        stay=StayDuration(date.today() + timedelta(days=2), date.today() + timedelta(days=4)),
        num_guests=1,
        status=BookingStatus.CHECKED_IN,
        payment_received=True
    )
    repo = FakeRepo(booking)
    use_case = CheckInBookingUseCase(repo)

    try:
        use_case.execute(booking.reference.value)
        assert False, "Expected DomainException"
    except DomainException:
        pass
