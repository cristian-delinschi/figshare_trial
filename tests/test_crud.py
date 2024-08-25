import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from app import models, schemas, crud

# Create a test SQLite database in memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def mock_auth():
    """Fixture to mock auth functions."""
    with patch('app.auth.get_password_hash') as mock_get_password_hash:
        yield mock_get_password_hash


@pytest.fixture
def mock_last_login_date():
    """Fixture to mock set_last_login_date function."""
    with patch('app.crud.set_last_login_date') as mock_set_last_login_date:
        yield mock_set_last_login_date


def test_create_account_success(db, mock_auth, mock_last_login_date):
    """Test create_account with success."""
    mock_auth.return_value = "hashed_password"

    account_data = schemas.AccountRegister(
        name="Test User",
        email="test@example.com",
        password="plaintextpassword"
    )

    account = crud.create_account(db, account_data)

    assert account.id is not None
    assert account.name == "Test User"
    assert account.email == "test@example.com"
    assert account.hashed_password == "hashed_password"

    mock_last_login_date.assert_called_once_with(db, email="test@example.com")


def test_create_account_duplicate_email(db, mock_auth, mock_last_login_date):
    """Test create_account with duplicate email."""
    mock_auth.return_value = "hashed_password"

    account_data = schemas.AccountRegister(
        name="Test User",
        email="test@example.com",
        password="plaintextpassword"
    )

    crud.create_account(db, account_data)

    with pytest.raises(Exception):
        crud.create_account(db, account_data)


@pytest.fixture
def create_test_account(db: db):
    """Fixture to create a test account in the database."""

    def _create_test_account(name, email, password):
        hashed_password = "hashedpassword"
        account = models.Account(
            name=name,
            email=email,
            password=password,
            hashed_password=hashed_password
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    return _create_test_account


def test_get_accounts_empty(db: db):
    """Test get_accounts when there are no accounts in the database."""
    accounts = crud.get_accounts(db)
    assert len(accounts) == 0


def test_get_accounts_with_data(db: db, create_test_account):
    """Test get_accounts when there are multiple accounts in the database."""
    account1 = create_test_account(name="User1", email="user1@example.com", password="password1")
    account2 = create_test_account(name="User2", email="user2@example.com", password="password2")

    accounts = crud.get_accounts(db)
    assert len(accounts) == 2
    assert account1 in accounts
    assert account2 in accounts


def test_get_account_by_id(db: db, create_test_account):
    """Test get_account_by_id with a valid and an invalid ID."""
    account = create_test_account(name="User1", email="user1@example.com", password="password1")

    fetched_account = crud.get_account_by_id(db, acc_id=account.id)
    assert fetched_account is not None
    assert fetched_account.id == account.id

    non_existent_account = crud.get_account_by_id(db, acc_id=999)
    assert non_existent_account is None


def test_get_account_by_email(db: db, create_test_account):
    """Test get_account_by_email with a valid and an invalid email."""
    account = create_test_account(name="User1", email="user1@example.com", password="password1")

    fetched_account = crud.get_account_by_email(db, email="user1@example.com")
    assert fetched_account is not None
    assert fetched_account.email == account.email

    non_existent_account = crud.get_account_by_email(db, email="nonexistent@example.com")
    assert non_existent_account is None


def test_update_account_partial_update(db: db, create_test_account):
    """Test partially updating an account (only one field)."""
    create_test_account(name="Test User", email="test@example.com", password="password123")

    account_update = schemas.AccountPartialUpdate(name="New Name")  # Only updating the name
    updated_account = crud.update_account(db, email="test@example.com", account_update=account_update)

    assert updated_account is not None
    assert updated_account.name == "New Name"
    assert updated_account.email == "test@example.com"


def test_update_account_nonexistent(db: db):
    """Test trying to update a non-existent account."""
    account_update = schemas.AccountPartialUpdate(name="Non-existent User")
    updated_account = crud.update_account(db, email="nonexistent@example.com", account_update=account_update)

    assert updated_account is None


def test_update_account_no_update(db: db, create_test_account):
    """Test updating an account with no changes."""
    create_test_account(name="Test User", email="test@example.com", password="password123")

    account_update = schemas.AccountPartialUpdate()
    updated_account = crud.update_account(db, email="test@example.com", account_update=account_update)

    assert updated_account is not None
    assert updated_account.name == "Test User"
    assert updated_account.email == "test@example.com"


def test_update_account_multiple_fields(db: db, create_test_account):
    """Test updating multiple fields of an account."""
    create_test_account(name="Test User", email="test@example.com", password="password123")

    account_update = schemas.AccountPartialUpdate(name="Updated Name", password="newpassword")
    updated_account = crud.update_account(db, email="test@example.com", account_update=account_update)

    assert updated_account is not None
    assert updated_account.name == "Updated Name"
    assert updated_account.email == "test@example.com"


def test_delete_account_success(db: db, create_test_account):
    """Test deleting an existing account successfully."""
    create_test_account(name="Test User", email="test@example.com", password="password123")

    deleted_account = crud.delete_account(db, email="test@example.com")

    assert deleted_account is not None
    assert deleted_account.email == "test@example.com"

    account_after_deletion = db.query(models.Account).filter(models.Account.email == "test@example.com").first()
    assert account_after_deletion is None


def test_delete_account_nonexistent(db: db):
    """Test trying to delete a non-existent account."""
    deleted_account = crud.delete_account(db, email="nonexistent@example.com")

    assert deleted_account is None
