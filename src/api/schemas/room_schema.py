from pydantic import BaseModel


class AvailableRoomResponse(BaseModel):
    room_number: str
    room_type: str
    capacity: int
    price_per_night: int
