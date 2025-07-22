from pydantic import BaseModel


class GuestRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    age: int


class GuestResponse(BaseModel):
    guest_id: str
    full_name: str
    email: str


class BookingSummary(BaseModel):
    reference: str
    room_number: str
    status: str
    check_in: str
    check_out: str
