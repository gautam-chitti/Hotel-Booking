from uuid import UUID

from sqlalchemy.orm import Session

from src.application.interfaces.guest_repository import IGuestRepository
from src.domain.entities.guest import Guest
from src.domain.value_objects.guest_age import GuestAge
from src.infrastructure.models.guest_model import GuestModel


class GuestRepositoryImpl(IGuestRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, guest_id: str) -> Guest | None:
        guest = self.session.query(GuestModel).filter_by(id=guest_id).first()
        if not guest:
            return None
        return Guest(
            guest_id=UUID(guest.id),
            full_name=guest.full_name,
            email=guest.email,
            phone=guest.phone,
            age=GuestAge(int(guest.age))
        )
    def save(self, guest: Guest) -> None:
        from infrastructure.models.guest_model import GuestModel

        model = GuestModel(
            id=str(guest.guest_id),
            full_name=guest.full_name,
            email=guest.email,
            phone=guest.phone,
            age=guest.age.value
        )
        self.session.add(model)
        self.session.commit()
