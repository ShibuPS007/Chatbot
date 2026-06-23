from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models import Chat, Message
from backend.services.gemini_service import get_gemini_model
from backend.services.embedding_service import retrieve, collection
def create_chat(db: Session, user_id: str, title: str):
    chat = Chat(title=title or "New Chat", user_id=user_id)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_user_chats(db: Session, user_id: str):
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
        .all()
    )


def get_chat_messages(db: Session, user_id: str, chat_id: str):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()

    if not chat:
        raise HTTPException(status_code=403, detail="Not your chat")

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp)
        .all()
    )


def send_message(db: Session, user_id: str, chat_id: str, content: str):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your chat")

    # Save user message
    db.add(Message(chat_id=chat_id, role="user", content=content))
    db.commit()
    
    # Load full history
    history = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp)
        .all()
    )

    # Rename chat after first message
    if len(history) == 1:
        chat.title = content[:30]
        db.commit()
    previous_messages=history[:-1]
    # Convert history to Gemini format
    chat_history = []

    for message in previous_messages:
        role = "user" if message.role == "user" else "model"

        chat_history.append({"role": role, "parts": [message.content]})


    model = get_gemini_model()
    chat_session = model.start_chat(history=chat_history)

    try:
        context = ""

        if collection.count() > 0:
            chunks = retrieve(content,user_id)

            if chunks:
                context = "\n\n".join(chunks)

        prompt = f"""
    Relevant context:
    {context}

    User question:
    {content}

    Instructions:
    - Use the context if it is useful.
    - Ignore it if it is irrelevant.
    """

        response = chat_session.send_message(prompt)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response"
        )

    # Save assistant reply
    db.add(Message(chat_id=chat_id, role="assistant", content=response.text))

    db.commit()

    return {"reply": response.text}
