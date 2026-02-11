from .conftest import client

def test_signup():
    res = client.post(
        "/signup",
        json={"email": "auth@test.com", "password": "password123"}
    )

    data = res.json()
    assert res.status_code == 200
    assert "user_id" in data
    assert "access_token" in data


def test_login():
    # first create user
    client.post(
        "/signup",
        json={"email": "login@test.com", "password": "secret"}
    )

    # then login
    res = client.post(
        "/login",
        json={"email": "login@test.com", "password": "secret"}
    )

    data = res.json()
    assert res.status_code == 200
    assert "access_token" in data
