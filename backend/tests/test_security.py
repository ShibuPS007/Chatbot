from .conftest import client, get_test_token

def test_chat_access_restricted():
    # User 1 creates chat
    token1 = get_test_token("user1@test.com")

    chat_res = client.post(
        "/chats",
        json={},
        headers={"token": token1}
    )
    chat_id = chat_res.json()["id"]

    # User 2 logs in
    token2 = get_test_token("user2@test.com")

    # User 2 tries to access User 1's chat
    res = client.get(
        f"/chats/{chat_id}",
        headers={"token": token2}
    )

    assert res.status_code == 403
