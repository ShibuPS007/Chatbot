def get_token(client):

    response = client.post(
        "/signup", json={"email": "user@test.com", "password": "123456"}
    )

    return response.json()["access_token"]


def test_create_chat(client):

    token = get_token(client)

    response = client.post(
        "/chats",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Chat"},
    )

    assert response.status_code == 200


def test_get_chats(client):

    token = get_token(client)

    client.post(
        "/chats", headers={"Authorization": f"Bearer {token}"}, json={"title": "Chat 1"}
    )

    response = client.get("/chats", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
