from dataclasses import dataclass

from src.domain.exceptions import DomainException


@dataclass(frozen=True)
class GuestAge:
    value: int

    def __post_init__(self):
        if self.value < 18:
            raise DomainException("Guest must be at least 18 years old.")
