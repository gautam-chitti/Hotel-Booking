from datetime import date

from pydantic import BaseModel


class BookingRequest(BaseModel):
    guest_id: str
    room_number: str
    num_guests: int
    check_in: date
    check_out: date


class BookingResponse(BaseModel):
    reference: str
    status: str
    room_number: str
    check_in: date
    check_out: date
    total_price: int

class BookingDetailsResponse(BaseModel):
    reference: str
    guest_name: str
    guest_email: str
    room_number: str
    room_type: str
    check_in: date
    check_out: date
    status: str
    total_price: int

