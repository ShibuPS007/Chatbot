from unittest.mock import MagicMock

from backend.models import User
from backend.services.chat_service import create_chat, get_user_chats, send_message


def test_create_chat(db):

    user = User(email="test@test.com", hashed_password="hashed")

    db.add(user)
    db.commit()

    chat = create_chat(db=db, user_id=user.id, title="My Chat")

    assert chat.title == "My Chat"
    assert chat.user_id == user.id


def test_get_user_chats(db):

    user = User(email="test@test.com", hashed_password="hashed")

    db.add(user)
    db.commit()

    create_chat(db, user.id, "Chat 1")
    create_chat(db, user.id, "Chat 2")

    chats = get_user_chats(db, user.id)

    assert len(chats) == 2


def test_send_message(db, mocker):

    user = User(email="test@test.com", hashed_password="hashed")

    db.add(user)
    db.commit()

    chat = create_chat(db=db, user_id=user.id, title="New Chat")

    fake_response = MagicMock()
    fake_response.text = "Hello from Gemini"

    fake_chat_session = MagicMock()
    fake_chat_session.send_message.return_value = fake_response

    fake_model = MagicMock()
    fake_model.start_chat.return_value = fake_chat_session

    mocker.patch(
        "backend.services.chat_service.get_gemini_model", return_value=fake_model
    )

    result = send_message(db=db, user_id=user.id, chat_id=chat.id, content="Hi")

    assert result["reply"] == "Hello from Gemini"


def test_user_cannot_access_other_chat(client):

    # User 1
    response1 = client.post(
        "/signup",
        json={"email": "user1@test.com", "password": "123456"},
    )

    token1 = response1.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    chat_response = client.post(
        "/chats",
        json={"title": "Secret Chat"},
        headers=headers1,
    )

    chat_id = chat_response.json()["id"]

    # User 2
    response2 = client.post(
        "/signup",
        json={"email": "user2@test.com", "password": "123456"},
    )

    token2 = response2.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    response = client.get(
        f"/chats/{chat_id}",
        headers=headers2,
    )

    assert response.status_code == 403