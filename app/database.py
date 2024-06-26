# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


#DATABASE CONSTANTS
DB_USER = config('DB_USER')
DB_PWD = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')

#DATABASE CREATION
URL = f"postgresql://{DB_USER}:{DB_PWD}@localhost/{DB_NAME}"
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the session for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()










