from unittest.mock import MagicMock


def test_signup_login_flow(client):
    # Signup
    signup_response = client.post(
        "/signup", json={"email": "user@test.com", "password": "123456"}
    )

    assert signup_response.status_code == 200

    # Login
    login_response = client.post(
        "/login", json={"email": "user@test.com", "password": "123456"}
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data


def test_create_chat_flow(client):

    signup_response = client.post(
        "/signup", json={"email": "user@test.com", "password": "123456"}
    )

    token = signup_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_chat_response = client.post(
        "/chats", json={"title": "My Chat"}, headers=headers
    )

    assert create_chat_response.status_code == 200

    list_chats_response = client.get("/chats", headers=headers)

    assert list_chats_response.status_code == 200
    assert len(list_chats_response.json()) == 1


def test_get_chat_messages_flow(client):

    signup_response = client.post(
        "/signup", json={"email": "user@test.com", "password": "123456"}
    )

    token = signup_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    chat_response = client.post("/chats", json={"title": "Test Chat"}, headers=headers)

    chat_id = chat_response.json()["id"]

    messages_response = client.get(f"/chats/{chat_id}", headers=headers)

    assert messages_response.status_code == 200
    assert messages_response.json() == []


def test_send_message_flow(client, mocker):

    # Mock Gemini
    fake_response = MagicMock()
    fake_response.text = "Hello from Gemini"

    fake_chat_session = MagicMock()
    fake_chat_session.send_message.return_value = fake_response

    fake_model = MagicMock()
    fake_model.start_chat.return_value = fake_chat_session

    mocker.patch(
        "backend.services.chat_service.get_gemini_model", return_value=fake_model
    )

    # Signup
    signup_response = client.post(
        "/signup", json={"email": "user@test.com", "password": "123456"}
    )

    token = signup_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create chat
    chat_response = client.post("/chats", json={"title": "New Chat"}, headers=headers)

    chat_id = chat_response.json()["id"]

    # Send message
    response = client.post(
        f"/chats/{chat_id}", json={"content": "Hello"}, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["reply"] == "Hello from Gemini"

    # Verify history contains both user and assistant messages
    history_response = client.get(f"/chats/{chat_id}", headers=headers)

    history = history_response.json()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_protected_route_without_token(client):

    response = client.get("/chats")

    assert response.status_code == 401
