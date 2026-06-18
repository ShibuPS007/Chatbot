from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.auth import get_current_user
from backend.schemas import ChatResponse, MessageResponse, MessageCreate, ChatCreate,ReplyResponse

from backend.services import chat_service

router = APIRouter()


@router.post("/chats", response_model=ChatResponse)
def create_chat_route(
    data: ChatCreate, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return chat_service.create_chat(db=db, user_id=user.id, title=data.title)


@router.get("/chats", response_model=list[ChatResponse])
def get_chats_route(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return chat_service.get_user_chats(db=db, user_id=user.id)


@router.get("/chats/{chat_id}", response_model=list[MessageResponse])
def get_messages_route(
    chat_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return chat_service.get_chat_messages(db=db, user_id=user.id, chat_id=chat_id)


@router.post("/chats/{chat_id}",response_model=ReplyResponse)
def send_message_route(
    chat_id: str,
    msg: MessageCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return chat_service.send_message(
        db=db, user_id=user.id, chat_id=chat_id, content=msg.content
    )
