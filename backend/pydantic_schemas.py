from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatCreate(BaseModel):
    title: str | None = "New Chat"

class ChatResponse(BaseModel):
    id: str
    title: str
    created_at: datetime

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    chat_id: str
    role: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class ReplyResponse(BaseModel):
    reply: str

class UserCreate(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
