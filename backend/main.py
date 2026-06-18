from fastapi import FastAPI

from backend.database import Base, engine
from backend.routers.auth_router import router as auth_router
from backend.routers.chat_router import router as chat_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)

Base.metadata.create_all(bind=engine)

print("🚀 BACKEND VERSION 3 LOADED")
