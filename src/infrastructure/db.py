from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite file-based DB
DATABASE_URL = "sqlite:///src/infrastructure/hotel.db"

# Set echo=True for debugging SQL
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
