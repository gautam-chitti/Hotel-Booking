from sqlalchemy.orm import Session

from src.application.interfaces.booking_repository import IBookingRepository
from src.domain.entities.booking import Booking
from src.domain.enums import BookingStatus
from src.infrastructure.models.booking_model import BookingModel


class BookingRepositoryImpl(IBookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, booking: Booking) -> None:
        booking_record = BookingModel(
            reference=booking.reference.value,
            guest_id=str(booking.guest.guest_id),
            room_number=booking.room.room_number,
            check_in_date=booking.stay.check_in,
            check_out_date=booking.stay.check_out,
            num_guests=booking.num_guests,
            status=booking.status,
            payment_received=booking.payment_received
        )
        self.session.add(booking_record)
        self.session.commit()

    def is_room_available(self, room_number: str, check_in, check_out) -> bool:
        overlapping = self.session.query(BookingModel).filter(
            BookingModel.room_number == room_number,
            BookingModel.status == BookingStatus.BOOKED,
            BookingModel.check_out_date > check_in,
            BookingModel.check_in_date < check_out
        ).first()
        return overlapping is None
    
    def get_by_reference(self, reference: str) -> Booking | None:
        record = self.session.query(BookingModel).filter_by(reference=reference).first()
        if not record:
            return None

        # Convert back to domain Booking (using Guest + Room)
        from infrastructure.repositories.guest_repository_impl import GuestRepositoryImpl
        from infrastructure.repositories.room_repository_impl import RoomRepositoryImpl

        guest_repo = GuestRepositoryImpl(self.session)
        room_repo = RoomRepositoryImpl(self.session)

        guest = guest_repo.get_by_id(record.guest_id)
        room = room_repo.get_by_number(record.room_number)

        from domain.entities.booking import Booking
        from domain.value_objects.booking_reference import BookingReference
        from domain.value_objects.stay_duration import StayDuration

        return Booking(
            reference=BookingReference(record.reference),
            guest=guest,
            room=room,
            stay=StayDuration(record.check_in_date, record.check_out_date),
            num_guests=record.num_guests,
            status=record.status,
            payment_received=record.payment_received
        )

    def update(self, booking: Booking) -> None:
        record = self.session.query(BookingModel).filter_by(reference=booking.reference.value).first()
        if not record:
            raise Exception("Booking not found during update")

        record.status = booking.status
        self.session.commit()

    def get_by_guest_id(self, guest_id: str) -> list[Booking]:
        from domain.entities.booking import Booking
        from domain.value_objects.booking_reference import BookingReference
        from domain.value_objects.stay_duration import StayDuration
        from infrastructure.repositories.guest_repository_impl import GuestRepositoryImpl
        from infrastructure.repositories.room_repository_impl import RoomRepositoryImpl

        guest_repo = GuestRepositoryImpl(self.session)
        room_repo = RoomRepositoryImpl(self.session)

        records = self.session.query(BookingModel).filter_by(guest_id=guest_id).all()
        bookings = []
        for r in records:
            guest = guest_repo.get_by_id(r.guest_id)
            room = room_repo.get_by_number(r.room_number)
            bookings.append(Booking(
                reference=BookingReference(r.reference),
                guest=guest,
                room=room,
                stay=StayDuration(r.check_in_date, r.check_out_date),
                num_guests=r.num_guests,
                status=r.status,
                payment_received=r.payment_received
            ))
        return bookings
