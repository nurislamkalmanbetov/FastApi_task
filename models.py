from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID
import uuid 
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship



Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(SmallInteger, nullable=False)
    updated_at = Column(SmallInteger, nullable=False)

    chats = relationship('Chat', secondary='user_chats', back_populates='users')


class ChatStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2
    ARCHIVED = 3

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(SmallInteger, default=ChatStatus.ACTIVE.value, nullable=False)
    updated_at = Column(SmallInteger, nullable=False)

    users = relationship('User', secondary='user_chats', back_populates='chats')


class UserChat(Base):
    __tablename__ = 'user_chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=False)
    time_delivered = Column(DateTime, default=datetime.utcnow, nullable=False)
    time_seen = Column(DateTime)
    is_delivered = Column(Boolean, default=False, nullable=False)
