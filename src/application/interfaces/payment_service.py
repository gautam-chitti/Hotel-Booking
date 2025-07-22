from abc import ABC, abstractmethod

from src.domain.entities.booking import Booking


class IPaymentService(ABC):

    @abstractmethod
    def process_payment(self, booking: Booking) -> bool:
        pass
