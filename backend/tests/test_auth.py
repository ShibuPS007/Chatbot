from backend.auth import hash_password, verify_password, create_access_token


def test_hash_password():
    password = "secret123"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password():
    password = "secret123"

    hashed = hash_password(password)

    assert verify_password(password, hashed)


def test_create_access_token():
    token = create_access_token({"sub": "123"})

    assert token is not None
    assert isinstance(token, str)

def test_duplicate_signup(client):

    client.post(
        "/signup",
        json={"email": "user@test.com", "password": "123456"},
    )

    response = client.post(
        "/signup",
        json={"email": "user@test.com", "password": "123456"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

def test_invalid_login(client):

    client.post(
        "/signup",
        json={"email": "user@test.com", "password": "123456"},
    )

    response = client.post(
        "/login",
        json={"email": "user@test.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_invalid_token(client):

    response = client.get(
        "/chats",
        headers={"Authorization": "Bearer fake_token"},
    )

    assert response.status_code == 401


