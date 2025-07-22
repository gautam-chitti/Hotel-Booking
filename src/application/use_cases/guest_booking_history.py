from src.application.interfaces.booking_repository import IBookingRepository
from src.domain.entities.booking import Booking


class GuestBookingHistoryUseCase:
    def __init__(self, repo: IBookingRepository):
        self.repo = repo

    def execute(self, guest_id: str) -> list[Booking]:
        return self.repo.get_by_guest_id(guest_id)
