import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, models
from app.database import get_db

# In-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Initialize the database
@pytest.fixture(scope="module")
def setup_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_register(setup_db):
    response = client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_register_existing_email(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    response = client.post("/register/", data={
        "name": "Another User",
        "email": "testuser@example.com",
        "password": "password456"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_get_accounts(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    token_response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "password123"
    })
    token = token_response.json()["access_token"]
    response = client.get("/accounts/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_account(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    token_response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "password123"
    })
    token = token_response.json()["access_token"]
    response = client.get(
        "/account/1/",
        params={"acc_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    account = response.json()

    assert account["email"] == "testuser@example.com"
    assert account["name"] == "Test User"

    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_full_update_account(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    })
    token_response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "password123"
    })
    token = token_response.json()["access_token"]
    response = client.put("/account_full_update", data={
        "email": "testuser@example.com",
        "name": "Updated User",
        "password": "newpassword1234",
        "is_active": "False",
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated User"
    assert response.json()["is_active"] is False


def test_partial_update_account(setup_db):
    client.post("/register/", data={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    })
    token_response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "password123"
    })
    token = token_response.json()["access_token"]

    response = client.patch("/account_partial_update", data={
        "email": "testuser@example.com",
        "is_active": "False",
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["name"] == "Updated User"
    assert response.json()["is_active"] is False
