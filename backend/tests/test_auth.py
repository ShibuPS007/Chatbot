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
