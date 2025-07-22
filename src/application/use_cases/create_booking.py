from src.application.dtos.booking_dto import CreateBookingDTO
from src.application.interfaces.booking_repository import IBookingRepository
from src.application.interfaces.payment_service import IPaymentService
from src.domain.entities.booking import Booking
from src.domain.exceptions import DomainException
from src.domain.value_objects.booking_reference import BookingReference
from src.domain.value_objects.stay_duration import StayDuration


class CreateBookingUseCase:
    def __init__(self, booking_repo: IBookingRepository, payment_service: IPaymentService):
        self.booking_repo = booking_repo
        self.payment_service = payment_service

    def execute(self, dto: CreateBookingDTO, guest, room) -> Booking:
        if not self.booking_repo.is_room_available(dto.room_number, dto.check_in, dto.check_out):
            raise DomainException("Room is not available for the selected dates.")

        stay = StayDuration(dto.check_in, dto.check_out)
        ref = BookingReference.generate()

        # Booking: status is BOOKED, but payment_received must be True
        booking = Booking(
            reference=ref,
            guest=guest,
            room=room,
            stay=stay,
            num_guests=dto.num_guests,
            payment_received=True
        )

        # Process Payment (Mocked)
        if not self.payment_service.process_payment(booking):
            raise DomainException("Payment failed.")
        booking.payment_received = True

        # Save booking
        self.booking_repo.save(booking)

        return booking
