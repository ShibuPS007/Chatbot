import os
from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from backend.database import Base, engine, SessionLocal
from backend.models import Chat, Message, User
import google.generativeai as genai
from dotenv import load_dotenv
from backend.pydantic_schemas import ChatResponse, MessageResponse, MessageCreate, UserCreate, LoginRequest, ChatCreate
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-flash-latest")

Base.metadata.create_all(bind=engine)

app = FastAPI()
print("🚀 BACKEND VERSION 3 LOADED")

# ---------- DB DEPENDENCY ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")


# ---------- PASSWORD HASHING ----------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# ---------- ROUTES ----------

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        return {"error": "Email already exists"}

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})

    return {
        "user_id": new_user.id,
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": str(user.id)})

    return {
        "user_id": user.id,
        "access_token": token,
        "token_type": "bearer"
    }

# ---------- CHAT ROUTES (PROTECTED) ----------

@app.post("/chats", response_model=ChatResponse)
def create_chat(
    data: ChatCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = Chat(title=data.title or "New Chat", user_id=user.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@app.get("/chats", response_model=list[ChatResponse])
def get_chats(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.created_at.desc())
        .all()
    )
    return chats

@app.get("/chats/{chat_id}", response_model=list[MessageResponse])
def get_messages(
    chat_id: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # 🔐 ONE query that proves ownership in one shot
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id, Chat.user_id == user.id)
        .first()
    )

    # If nothing is returned → either chat doesn't exist
    # OR it doesn't belong to this user → treat as forbidden
    if not chat:
        raise HTTPException(status_code=403, detail="Not your chat")

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp)
        .all()
    )


@app.post("/chats/{chat_id}")
def send_message(
    chat_id: str,
    msg: MessageCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if chat.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your chat")


    db.add(Message(chat_id=chat_id, role="user", content=msg.content))
    db.commit()

    history = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp)
        .all()
    )

    if len(history) == 1:
        chat.title = msg.content[:30]
        db.commit()

    chat_history = []
    for m in history:
        role = "user" if m.role == "user" else "model"
        chat_history.append({"role": role, "parts": [m.content]})

    chat = model.start_chat(history=chat_history)
    response = chat.send_message(msg.content)

    db.add(Message(chat_id=chat_id, role="assistant", content=response.text))
    db.commit()

    return {"reply": response.text}
