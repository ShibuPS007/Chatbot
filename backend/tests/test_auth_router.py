def test_signup(client):

    response = client.post(
        "/signup", json={"email": "user@test.com", "password": "123456"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def test_login(client):

    client.post("/signup", json={"email": "user@test.com", "password": "123456"})

    response = client.post(
        "/login", json={"email": "user@test.com", "password": "123456"}
    )

    assert response.status_code == 200
