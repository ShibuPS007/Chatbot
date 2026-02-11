from .conftest import client, get_test_token

def test_create_chat_requires_auth():
    res = client.post("/chats", json={})
    assert res.status_code in [401, 422]


def test_create_chat_with_auth():
    token = get_test_token("chat1@test.com")

    res = client.post(
        "/chats",
        json={},
        headers={"token": token}
    )

    data = res.json()
    assert res.status_code == 200
    assert "id" in data
    assert data["title"] == "New Chat"


def test_send_message_flow():
    token = get_test_token("chat2@test.com")

    # create chat
    chat_res = client.post(
        "/chats",
        json={},
        headers={"token": token}
    )
    chat_id = chat_res.json()["id"]

    # send message
    res = client.post(
        f"/chats/{chat_id}",
        json={"content": "Hello from test"},
        headers={"token": token}
    )

    data = res.json()
    assert res.status_code == 200
    assert "reply" in data
