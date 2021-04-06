from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import DATA_BASE_URL

engine = create_engine(DATA_BASE_URL)
session_local = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
