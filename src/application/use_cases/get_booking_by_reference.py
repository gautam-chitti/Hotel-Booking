from src.application.interfaces.booking_repository import IBookingRepository
from src.domain.entities.booking import Booking
from src.domain.exceptions import DomainException


class GetBookingByReferenceUseCase:
    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def execute(self, reference: str) -> Booking:
        booking = self.repo.get_by_reference(reference)
        if not booking:
            raise DomainException("Booking not found")
        return booking
