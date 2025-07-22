#!/bin/bash
set -e

echo "Setting Up Hotel Booking System"

echo "Building a virtual environment"
uv venv .venv

echo "Activating virtual environment"
source .venv/Scripts/activate

echo "Installing the dependencies"
uv pip install fastapi uvicorn sqlalchemy pydantic pytest pytest-cov ruff pyre-check

echo "Creating folder structure"
mkdir -p src/domain src/application src/infrastructure src/api
mkdir -p tests/domain tests/application tests/infrastructure tests/api
mkdir -p scripts
cd domain
mkdir entities 
mkdir value_objects
cd ..

echo " ...Creating the Files...  "
touch src/domain/__init__.py
touch src/domain/enums.py
touch src/domain/exceptions.py
touch src/domain/entities/__init__.py
touch src/domain/entities/room.py
touch src/domain/entities/guest.py
touch src/domain/value_objects/__init__.py
touch src/domain/value_objects/booking_reference.py
touch src/domain/value_objects/stay_duration.py
touch src/domain/value_objects/guest_age.py
touch src/domain/value_objects/room_capacity.py
touch src/domain/value_objects/room_capacity.py
touch src/api/main.py
cd src
cd application
mkdir dtos
mkdir use_cases
mkdir interfaces

cd ..
cd ..

touch src/application/use_cases/__init__.py
touch src/application/use_cases/create_booking.py
touch tests/application/use_cases/test_create_booking.py

touch src/application/use_cases/get_booking_by_reference.py
touch tests/application/use_cases/test_get_booking_by_reference.py

touch src/application/use_cases/cancel_booking.py
touch tests/application/use_cases/test_cancel_booking.py

touch src/application/use_cases/check_in_booking.py
touch tests/application/use_cases/test_check_in_booking.py


touch src/application/use_cases/check_out_booking.py
touch tests/application/use_cases/test_check_out_booking.py

touch src/application/use_cases/check_room_availability.py
touch tests/application/use_cases/test_check_room_availability.py

touch src/application/use_cases/register_guest.py
touch tests/application/use_cases/test_register_guest.py

touch src/application/use_cases/guest_booking_history.py
touch tests/application/use_cases/test_guest_booking_history.py


touch src/application/dtos/__init__.py
touch src/application/dtos/booking_dto.py
touch src/application/interfaces/__init__.py
touch src/application/interfaces/room_repository.py
touch src/application/interfaces/guest_repository.py
touch src/application/interfaces/booking_repository.py
touch src/application/interfaces/payment_repository.py

cd src
cd infrastructure

mkdir repositories
mkdir services
mkdir models

cd ..
cd ..


touch src/infrastructure/repositories/__init__.py
touch src/infrastructure/repositories/booking_repository_impl.py
touch src/infrastructure/repositories/room_repository_impl.py
touch src/infrastructure/repositories/guest_repository_impl.py 
touch src/infrastructure/services/mock_payment_service.py
touch src/infrastructure/models/__init__.py
touch src/infrastructure/models/base.py
touch src/infrastructure/models/guest_model.py
touch src/infrastructure/models/room_model.py
touch src/infrastructure/models/booking_model.py

touch src/infrastructure/db.py
touch src/infrastructure/base.py

cd src 
cd api

mkdir routes
mkdir dependencies
mkdir schemas

touch routes/__init__.py
touch routes/booking_routes.py
touch dependencies/db.py
touch schemas/booking_schema.py 
touch schemas/room_schema.py
touch schemas/guest_schema.py

cd ..
cd ..


echo "...Creating the SQLite db..."
touch src/infrastructure/hotel.db

echo "Setup complete!"



python -c 'from infrastructure.models.base import Base; from infrastructure.db import engine; import infrastructure.models.booking_model; Base.metadata.create_all(bind=engine)'