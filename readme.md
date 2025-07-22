# 🏨 Hotel Booking System (FastAPI + DDD Architecture)

A simplified hotel management system that allows guests to register, book rooms, check-in, check-out, and view booking history. Built using **FastAPI**, **SQLAlchemy**, and a clean **Domain-Driven Design (DDD)** approach.

---

## ✅ Features

- Register a new guest
- Book a room with payment
- View room availability
- Cancel booking
- Check-in and Check-out
- View guest booking history

---

## ⚙️ Prerequisites

- Python 3.10+
- `uv` package manager (`pip install uv`)
- Git (for cloning)
- Unix-like shell (for running `.sh` scripts — use Git Bash on Windows)

---

## 🛠️ Setup Instructions

Clone the repo and run the setup script:

```bash
git clone https://github.com/gautam-chitti/HotelBookingSystem.git
cd hotel-booking
sh scripts/setup.sh
```

This will:

- Create and activate a virtual environment using `uv`
- Install all dependencies
- Apply migrations to initialize the SQLite database

---

## 🚀 Run the Server

```bash
sh scripts/run.sh
```

FastAPI will start at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Swagger UI docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Run Tests + Type Checking

```bash
sh scripts/test.sh
```

This script:

- Runs all tests with `pytest`
- Checks for type safety using `pyre`
- Fails if test coverage < 70%
- Shows a coverage report summary

---

## 🧾 Sample API Usage (cURL)

### 📌 Register Guest

```bash
curl -X POST http://127.0.0.1:8000/guests -H "Content-Type: application/json" -d '{
"full_name": "John Doe",
"email": "john@example.com",
"phone": "1234567890",
"age": 30
}'
```

### 📌 Book a Room

```bash
curl -X POST http://127.0.0.1:8000/bookings -H "Content-Type: application/json" -d '{
"guest_id": "GUEST-ID-HERE",
"room_number": "101",
"num_guests": 2,
"check_in": "2025-07-20",
"check_out": "2025-07-22"
}'
```

### 📌 Check Room Availability

```bash
curl "http://127.0.0.1:8000/rooms/availability?check_in=2025-07-20&check_out=2025-07-22"
```

### 📌 Cancel Booking

```bash
curl -X DELETE http://127.0.0.1:8000/bookings/BOOKING-REF-HERE
```

---

```

├── scripts/
│   ├── setup.sh          # Install deps, create venv, migrate DB
│   ├── run.sh            # Run FastAPI server
│   └── test.sh           # Run tests, Pyre, coverage
├── src/
│   ├── api/              # FastAPI routes, schemas, DI
│   ├── application/      # Use cases, DTOs, interfaces
│   ├── domain/           # Core entities, value objectsexceptions
│   ├── infrastructure/   # DB, services, repository implementations
│   └── __init__.py
├── tests/                # Pytest unit & integration tests
├── pyproject.toml        # Dependencies & tooling
└── README.md
```

---
