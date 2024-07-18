# Third-party imports
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Internal imports
import datetime


#DATABASE DEFINITION
Base = declarative_base()

class Conversation(Base): 

    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=True)
    start_time = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    end_time = Column(DateTime, nullable=True)
    messages = relationship("Message", back_populates="conversation")
    

class Message(Base): 

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    sender = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    conversation = relationship("Conversation", back_populates="messages")




