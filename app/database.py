
# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
from typing import Generator, Optional

# Internal imports
from models import Conversation, Message
import datetime


#DATABASE CONSTANTS
DB_USER = config('DB_USER')
DB_PWD = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')

#DATABASE CREATION
DB_URL = f"postgresql://{DB_USER}:{DB_PWD}@localhost/{DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#DB Operations Definition

# Create a new conversation
def create_conversation(db:Session, user_id: Optional[str] = None) -> int:

    new_conversation = Conversation(user_id=user_id)
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation.id


# Add a message to a conversation
def add_message(db:Session, conversation_id: int, sender: str, message: str) -> None:

    new_message = Message(conversation_id=conversation_id, sender=sender, message=message)
    db.add(new_message)
    db.commit()
    

# Add a message to a conversation
def end_conversation(db:Session, conversation_id: int) -> None:

    conversation = db.query(Conversation).filter_by(id=conversation_id).first()
    conversation.end_time = datetime.datetime.now(datetime.timezone.utc)
    db.commit()




# Dependency to get the database session
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




