from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums import BookingStatus
from src.infrastructure.models.base import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    reference: Mapped[str] = mapped_column(String(10), primary_key=True, index=True)
    guest_id: Mapped[str] = mapped_column(String, ForeignKey("guests.id"), nullable=False)
    room_number: Mapped[str] = mapped_column(String, ForeignKey("rooms.room_number"), nullable=False)

    check_in_date: Mapped[str] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[str] = mapped_column(Date, nullable=False)

    num_guests: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.BOOKED)
    payment_received: Mapped[bool] = mapped_column(Boolean, default=False)
