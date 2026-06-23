from backend.main import app


def test_app_exists():
    assert app is not None


def test_chats_requires_auth(client):

    response = client.get("/chats")

    assert response.status_code == 401
