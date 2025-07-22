import uuid

from sqlalchemy.orm import Session

from infrastructure.db import SessionLocal
from infrastructure.models.guest_model import GuestModel
from infrastructure.models.room_model import RoomModel


def seed_rooms(session: Session):
    if session.query(RoomModel).first():
        print("Rooms already seeded.")
        return

    print("Seeding rooms...")

    def create_rooms(room_type, count, price, capacity, floor_start):
        for i in range(1, count + 1):
            room_number = f"{floor_start}{i:02d}"
            session.add(RoomModel(
                room_number=room_number,
                room_type=room_type,
                price_per_night=price,
                capacity=capacity
            ))

    create_rooms("Standard", 50, 100, 2, 1)
    create_rooms("Deluxe", 40, 200, 3, 2)
    create_rooms("Suite", 10, 300, 4, 3)

    session.commit()
    print("Rooms seeded.")


def seed_guests(session: Session):
    if session.query(GuestModel).first():
        print("Guests already seeded.")
        return

    print("Seeding guests...")

    sample_guests = [
        {"full_name": "Alice Johnson", "email": "alice@example.com", "phone": "1234567890", "age": 28},
        {"full_name": "Bob Singh", "email": "bob@example.com", "phone": "9876543210", "age": 35},
        {"full_name": "Charlie Patel", "email": "charlie@example.com", "phone": "1112223333", "age": 22},
    ]

    for guest in sample_guests:
        session.add(GuestModel(
            id=str(uuid.uuid4()),
            full_name=guest["full_name"],
            email=guest["email"],
            phone=guest["phone"],
            age=guest["age"]
        ))

    session.commit()
    print(" Guests seeded.")


def main():
    session = SessionLocal()
    try:
        seed_rooms(session)
        seed_guests(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
