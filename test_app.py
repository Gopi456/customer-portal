import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Reset application data before every test
    import app as application

    application.customers.clear()
    application.next_id = 1

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "UP"


def test_customer_registration(client):
    response = client.post(
        "/customers",
        json={
            "name": "Gopi",
            "email": "gopi@example.com"
        }
    )

    assert response.status_code == 201
    assert response.json["name"] == "Gopi"
    assert response.json["email"] == "gopi@example.com"


def test_get_customer(client):
    client.post(
        "/customers",
        json={
            "name": "Ravi",
            "email": "ravi@example.com"
        }
    )

    response = client.get("/customers/1")

    assert response.status_code == 200
    assert response.json["name"] == "Ravi"


def test_customer_not_found(client):
    response = client.get("/customers/999")

    assert response.status_code == 404
