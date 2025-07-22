from abc import ABC, abstractmethod

from src.domain.entities.booking import Booking


class IBookingRepository(ABC):

    @abstractmethod
    def save(self, booking: Booking) -> None:
        pass

    @abstractmethod
    def is_room_available(self, room_number: str, check_in, check_out) -> bool:
        pass
    @abstractmethod
    def get_by_reference(self, reference: str) -> Booking | None:
        pass
    @abstractmethod
    def update(self, booking: Booking) -> None:
        pass
    @abstractmethod
    def get_by_guest_id(self, guest_id: str) -> list[Booking]:
        pass

