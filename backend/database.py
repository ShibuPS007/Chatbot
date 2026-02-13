from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IN_DOCKER = os.path.exists("/.dockerenv")

if IN_DOCKER:
    DATABASE_URL = "sqlite:////app/backend/chat.db"
else:
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'chat.db')}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
