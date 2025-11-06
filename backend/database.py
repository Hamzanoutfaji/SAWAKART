from sqlmodel import create_engine, SQLModel, Session 

DB_USER = "hamza"
DB_PASS = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "webscraper_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)  # set echo=True for SQL debug

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
