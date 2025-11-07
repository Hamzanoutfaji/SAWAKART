import os
from sqlmodel import create_engine, SQLModel, Session

# Get the database URL from Render environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://hamza:QejZvdtu5QaD0hNBqDGxXXf8Yex4HBSF@dpg-d46kj8uuk2gs73886b70-a.frankfurt-postgres.render.com/webscraper_db_ml2x"
)

# Create the engine
engine = create_engine(DATABASE_URL, echo=False)  # Set echo=True for SQL debug

# Create tables if they don't exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Database session generator
def get_session():
    with Session(engine) as session:
        yield session
