from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date


from src.domain.exceptions import DomainException
from src.api.dependencies.db import get_db
from src.api.schemas.booking_schema import BookingDetailsResponse, BookingRequest, BookingResponse
from src.api.schemas.guest_schema import BookingSummary, GuestRequest, GuestResponse
from src.api.schemas.room_schema import AvailableRoomResponse
from src.application.dtos.booking_dto import CreateBookingDTO
from src.application.use_cases.cancel_booking import CancelBookingUseCase
from src.application.use_cases.check_in_booking import CheckInBookingUseCase
from src.application.use_cases.check_out_booking import CheckOutBookingUseCase
from src.application.use_cases.check_room_availability import CheckRoomAvailabilityUseCase
from src.application.use_cases.create_booking import CreateBookingUseCase
from src.application.use_cases.get_booking_by_reference import GetBookingByReferenceUseCase
from src.application.use_cases.guest_booking_history import GuestBookingHistoryUseCase
from src.application.use_cases.register_guest import RegisterGuestUseCase
from src.infrastructure.repositories.booking_repository_impl import BookingRepositoryImpl
from src.infrastructure.repositories.guest_repository_impl import GuestRepositoryImpl
from src.infrastructure.repositories.room_repository_impl import RoomRepositoryImpl
from src.infrastructure.services.mock_payment_service import MockPaymentService

router = APIRouter()


@router.post("/bookings", response_model=BookingResponse)
def create_booking(payload: BookingRequest, db: Session = Depends(get_db)):
    # Repositories & services
    booking_repo = BookingRepositoryImpl(db)
    guest_repo = GuestRepositoryImpl(db)
    room_repo = RoomRepositoryImpl(db)
    payment_service = MockPaymentService()

    # Fetch domain objects
    guest = guest_repo.get_by_id(payload.guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    room = room_repo.get_by_number(payload.room_number)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Prepare DTO
    dto = CreateBookingDTO(
        guest_id=payload.guest_id,
        room_number=payload.room_number,
        num_guests=payload.num_guests,
        check_in=payload.check_in,
        check_out=payload.check_out
    )

    # Use case
    use_case = CreateBookingUseCase(booking_repo, payment_service)
    booking = use_case.execute(dto, guest, room)

    return BookingResponse(
        reference=booking.reference.value,
        status=booking.status.value,
        room_number=booking.room.room_number,
        check_in=booking.stay.check_in,
        check_out=booking.stay.check_out,
        total_price=(booking.stay.check_out - booking.stay.check_in).days * booking.room.price_per_night
    )


@router.get("/bookings/{reference}", response_model=BookingDetailsResponse)
def get_booking(reference: str, db: Session = Depends(get_db)):
    repo = BookingRepositoryImpl(db)
    use_case = GetBookingByReferenceUseCase(repo)

    try:
        booking = use_case.execute(reference)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return BookingDetailsResponse(
        reference=booking.reference.value,
        guest_name=booking.guest.full_name,
        guest_email=booking.guest.email,
        room_number=booking.room.room_number,
        room_type=booking.room.room_type,
        check_in=booking.stay.check_in,
        check_out=booking.stay.check_out,
        status=booking.status.value,
        total_price=(booking.stay.check_out - booking.stay.check_in).days * booking.room.price_per_night
    )

@router.delete("/bookings/{reference}")
def cancel_booking(reference: str, db: Session = Depends(get_db)):
    repo = BookingRepositoryImpl(db)
    use_case = CancelBookingUseCase(repo)

    try:
        use_case.execute(reference)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Booking {reference} cancelled successfully"}


@router.post("/bookings/{reference}/check-in")
def check_in(reference: str, db: Session = Depends(get_db)):
    repo = BookingRepositoryImpl(db)
    use_case = CheckInBookingUseCase(repo)

    try:
        use_case.execute(reference)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Booking {reference} checked in successfully"}


@router.post("/bookings/{reference}/check-out")
def check_out(reference: str, db: Session = Depends(get_db)):
    repo = BookingRepositoryImpl(db)
    use_case = CheckOutBookingUseCase(repo)

    try:
        use_case.execute(reference)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Booking {reference} checked out successfully"}

@router.get("/rooms/availability", response_model=list[AvailableRoomResponse])
def get_available_rooms(
    check_in: date = Query(...),
    check_out: date = Query(...),
    db: Session = Depends(get_db)
):
    room_repo = RoomRepositoryImpl(db)
    booking_repo = BookingRepositoryImpl(db)
    use_case = CheckRoomAvailabilityUseCase(room_repo, booking_repo)

    rooms = use_case.execute(check_in, check_out)

    return [
        AvailableRoomResponse(
            room_number=r.room_number,
            room_type=r.room_type,
            capacity=r.capacity,
            price_per_night=r.price_per_night
        ) for r in rooms
    ]

@router.get("/rooms", response_model=list[AvailableRoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    room_repo = RoomRepositoryImpl(db)
    rooms = room_repo.list_all()
    
    return [
        AvailableRoomResponse(
            room_number=r.room_number,
            room_type=r.room_type,
            capacity=r.capacity,
            price_per_night=r.price_per_night
        ) for r in rooms
    ]


@router.post("/guests", response_model=GuestResponse)
def register_guest(payload: GuestRequest, db: Session = Depends(get_db)):
    repo = GuestRepositoryImpl(db)
    use_case = RegisterGuestUseCase(repo)

    guest = use_case.execute(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        age=payload.age
    )

    return GuestResponse(
        guest_id=str(guest.guest_id),
        full_name=guest.full_name,
        email=guest.email
    )


@router.get("/guests/{guest_id}/bookings", response_model=list[BookingSummary])
def get_guest_bookings(guest_id: str, db: Session = Depends(get_db)):
    repo = BookingRepositoryImpl(db)
    use_case = GuestBookingHistoryUseCase(repo)

    bookings = use_case.execute(guest_id)

    return [
        BookingSummary(
            reference=b.reference.value,
            room_number=b.room.room_number,
            status=b.status.value,
            check_in=str(b.stay.check_in),
            check_out=str(b.stay.check_out)
        )
        for b in bookings
    ]
