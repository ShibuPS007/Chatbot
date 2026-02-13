# backend/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine
import backend.main as main


client = TestClient(app)

# ---------- Shared DB setup for ALL tests ----------
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Fresh database before tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------- Shared helper for ALL tests ----------
def get_test_token(email):
    client.post(
        "/signup",
        json={"email": email, "password": "pass123"}
    )

    res = client.post(
        "/login",
        json={"email": email, "password": "pass123"}
    )

    return res.json()["access_token"]


# ---------- Mock Gemini (VERY IMPORTANT) ----------

class MockGeminiResponse:
    text = "Mock reply from Gemini"

class MockGeminiChat:
    def send_message(self, msg):
        return MockGeminiResponse()

def mock_start_chat(history=None):
    return MockGeminiChat()

# Replace real Gemini with mock
main.model.start_chat = mock_start_chat
