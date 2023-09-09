from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, User, Chat, Message, ChatStatus
from schemas import UserBase, ChatBase, MessageBase, UserCreate, UserDetail, ChatWithParticipant
from sqlalchemy.dialects.postgresql import UUID
import uuid
from uuid import UUID
from models import UserChat
from typing import List, Optional
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from fastapi import HTTPException





DATABASE_URL = "postgresql://postgres:qwerty123@localhost:5432/fastapitask"

Base.metadata.create_all(bind=create_engine(DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DATABASE_URL))

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/", response_model=List[UserBase])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [UserBase(name=user.name, status=user.status, updated_at=int(datetime.combine(user.updated_at, datetime.min.time()).timestamp())) for user in users]



# http://127.0.0.1:8000/user/?name=nuris
@app.get("/user/", response_model=UserDetail)
def get_user(db: Session = Depends(get_db), user_id: Optional[UUID] = None, name: Optional[str] = None):

    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    elif name:
        user = db.query(User).filter(User.name == name).first()
    else:
        raise HTTPException(status_code=400, detail="Необходимо указать либо id, либо имя для поиска пользователя")

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Преобразование datetime.date в timestamp после того, как user был извлечен
    date_object = user.updated_at
    timestamp = int(datetime.combine(date_object, datetime.min.time()).timestamp())
    
    return UserDetail(
        id=user.id,
        name=user.name,
        status=user.status,
        updated_at=timestamp
    )


# http://127.0.0.1:8000/user_chats/6233e8cb-06bd-43b3-9e17-10ff9ed4c2a7/
@app.get("/user_chats/{user_id}/", response_model=List[ChatWithParticipant])
def get_user_chats(user_id: UUID, db: Session = Depends(get_db), status: Optional[ChatStatus] = None):
    user_chats = db.query(UserChat).filter(UserChat.user_id == user_id).all()
    chat_ids = [uc.chat_id for uc in user_chats]

    # Если задан статус для фильтрации
    if status:
        chats = db.query(Chat).options(joinedload(Chat.users)).filter(Chat.id.in_(chat_ids), Chat.status == status.value).all()
    else:
        chats = db.query(Chat).options(joinedload(Chat.users)).filter(Chat.id.in_(chat_ids)).all()

    # Создаем список чатов с собеседниками
    results = []
    for chat in chats:
        for participant in chat.users:
            if participant.id != user_id:
                results.append(ChatWithParticipant(id=chat.id, name=chat.name, status=chat.status, updated_at=chat.updated_at, participant=participant))

    return results



@app.get("/users/{user_id}/chats", response_model=List[ChatBase])
def get_user_chats(user_id: UUID, status: Optional[int] = None, db: Session = Depends(get_db)):
    user_chats = db.query(UserChat).filter(UserChat.user_id == user_id).all()
    
    chat_ids = [uc.chat_id for uc in user_chats]
    chats_query = db.query(Chat).filter(Chat.id.in_(chat_ids))
    
    if status:
        chats_query = chats_query.filter(Chat.status == status)
    
    return chats_query.all()
    


@app.get("/chats/count", response_model=int)
def get_chats_count(status: Optional[int] = None, db: Session = Depends(get_db)):
    chats_query = db.query(Chat)
    
    if status:
        chats_query = chats_query.filter(Chat.status == status)
    
    return chats_query.count()



@app.get("/chats/{chat_id}/message_count", response_model=int)
def get_chat_message_count(chat_id: int, db: Session = Depends(get_db)):
    count = db.query(Message).filter_by(chat_id=chat_id).count()
    return count


# http://127.0.0.1:8000/messages/
@app.get("/messages/", response_model=List[MessageBase])
def get_messages(sender_id: Optional[UUID] = None, receiver_id: Optional[UUID] = None, time_delivered: Optional[datetime] = None, db: Session = Depends(get_db)):
    try:
        messages_query = db.query(Message)
    
        if sender_id:
            messages_query = messages_query.filter(Message.sender_id == sender_id)
        if receiver_id:
            messages_query = messages_query.filter(Message.receiver_id == receiver_id)
        if time_delivered:
            messages_query = messages_query.filter(Message.time_delivered == time_delivered)
    
        # Преобразование объектов ORM в объекты MessageBase
        return [MessageBase(**m.__dict__) for m in messages_query.all()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/chats/{chat_id}/message_count", response_model=int)
def get_chat_message_count(chat_id: int, db: Session = Depends(get_db)):
    count = db.query(Message).filter_by(chat_id=chat_id).count()
    return count

