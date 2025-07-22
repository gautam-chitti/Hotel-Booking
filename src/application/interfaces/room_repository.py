from abc import ABC, abstractmethod

from src.domain.entities.room import Room


class IRoomRepository(ABC):
    @abstractmethod
    def get_by_number(self, room_number: str) -> Room | None:
        pass
    @abstractmethod
    def list_all(self) -> list[Room]:
        pass
