from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import DATA_BASE_URL

engine = create_engine(DATA_BASE_URL)
session_local = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
