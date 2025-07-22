import pytest
from datetime import date, timedelta
from uuid import uuid4

from domain.entities.room import Room
from domain.entities.guest import Guest
from domain.value_objects.guest_age import GuestAge
from application.dtos.booking_dto import CreateBookingDTO
from application.use_cases.create_booking import CreateBookingUseCase
from domain.value_objects.booking_reference import BookingReference
from domain.exceptions import DomainException


class FakeBookingRepo:
    def __init__(self):
        self.saved = None

    def save(self, booking):
        self.saved = booking

    def is_room_available(self, room_number, check_in, check_out):
        return True


class CustomPaymentService:
    def process_payment(self, booking):
        booking.payment_received = True
        return True




def test_create_booking_success():
    room = Room(room_number="101", room_type="Standard")
    guest = Guest(
        guest_id=uuid4(),
        full_name="Test User",
        email="test@example.com",
        phone="9999999999",
        age=GuestAge(25)
    )

    check_in = date.today() + timedelta(days=2)
    check_out = date.today() + timedelta(days=5)

    dto = CreateBookingDTO(
        guest_id=str(guest.guest_id),
        room_number=room.room_number,
        num_guests=2,
        check_in=check_in,
        check_out=check_out
    )

    use_case = CreateBookingUseCase(FakeBookingRepo(), CustomPaymentService())
    booking = use_case.execute(dto, guest, room)

    assert booking.reference.value
    assert booking.status.name == "BOOKED"
    assert booking.payment_received is True
