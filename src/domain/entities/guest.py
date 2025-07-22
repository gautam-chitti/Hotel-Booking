from dataclasses import dataclass
from uuid import UUID

from src.domain.exceptions import DomainException
from src.domain.value_objects.guest_age import GuestAge


@dataclass(frozen=True)
class Guest:
    guest_id: UUID
    full_name: str
    email: str
    phone: str
    age: GuestAge

    def __post_init__(self):
        if not self.full_name or len(self.full_name.strip()) < 2:
            raise DomainException("Guest name must be at least 2 characters.")
        
        if "@" not in self.email or "." not in self.email:
            raise DomainException("Invalid email address.")

        if not self.phone.isdigit() or len(self.phone) < 10:
            raise DomainException("Phone number must be at least 10 digits.")
