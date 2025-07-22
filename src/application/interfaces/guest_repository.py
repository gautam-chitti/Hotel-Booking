from abc import ABC, abstractmethod

from src.domain.entities.guest import Guest


class IGuestRepository(ABC):
    @abstractmethod
    def get_by_id(self, guest_id: str) -> Guest | None:
        pass
    @abstractmethod
    def save(self, guest: Guest) -> None:
        pass
