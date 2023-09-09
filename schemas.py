from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import uuid
from datetime import datetime
from pydantic import validator


class UserBase(BaseModel):
    name: str
    status: int
    updated_at: datetime

class UserDetail(BaseModel):
    id: UUID
    name: str
    status: int
    updated_at: int

class UserCreate(UserBase):
    username: str
    email: str


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    name: str
    status: int
    updated_at: int 

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int

    class Config:
        orm_mode = True


class ChatWithParticipant(ChatBase):
    id: int
    participant: User

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    text: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    time_delivered: datetime
    time_seen: Optional[datetime]
    is_delivered: bool

    class Config:
        orm_mode = True
