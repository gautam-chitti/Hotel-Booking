import random
import string
from dataclasses import dataclass


@dataclass(frozen=True)
class BookingReference:
    value: str

    def __post_init__(self):
        if len(self.value) != 10 or not self.value.isalnum():
            raise ValueError("Booking reference must be a 10-character alphanumeric string.")

    @staticmethod
    def generate() -> "BookingReference":
        return BookingReference(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        )
