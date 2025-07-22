from src.application.interfaces.booking_repository import IBookingRepository
from src.domain.exceptions import DomainException


class CheckOutBookingUseCase:
    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def execute(self, reference: str):
        booking = self.repo.get_by_reference(reference)
        if not booking:
            raise DomainException("Booking not found")

        booking.check_out()
        self.repo.update(booking)
