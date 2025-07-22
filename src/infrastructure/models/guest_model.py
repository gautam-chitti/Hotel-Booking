from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.base import Base


class GuestModel(Base):
    __tablename__ = "guests"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(String, nullable=False)
