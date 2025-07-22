import uuid

from src.application.interfaces.guest_repository import IGuestRepository
from src.domain.entities.guest import Guest
from src.domain.value_objects.guest_age import GuestAge


class RegisterGuestUseCase:
    def __init__(self, repo: IGuestRepository):
        self.repo = repo

    def execute(self, full_name: str, email: str, phone: str, age: int) -> Guest:
        guest = Guest(
            guest_id=uuid.uuid4(),
            full_name=full_name,
            email=email,
            phone=phone,
            age=GuestAge(age)
        )
        self.repo.save(guest)
        return guest
