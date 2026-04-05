from sqlmodel import SQLModel, create_engine, Session

# SQLite file will be created in the root directory
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is required for SQLite in FastAPI
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Creates the database and tables based on your SQLModel classes."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI Dependency to inject database sessions into routes."""
    with Session(engine) as session:
        yield session
        