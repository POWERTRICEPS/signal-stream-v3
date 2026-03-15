import os 

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Provide a database session to API endpoints, ensuring it is properly closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

