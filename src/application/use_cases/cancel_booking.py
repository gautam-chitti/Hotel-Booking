from datetime import date

from src.application.interfaces.booking_repository import IBookingRepository
from src.domain.exceptions import DomainException


class CancelBookingUseCase:
    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def execute(self, reference: str):
        booking = self.repo.get_by_reference(reference)
        if not booking:
            raise DomainException("Booking not found")

        booking.cancel(today=date.today())
        self.repo.update(booking)
