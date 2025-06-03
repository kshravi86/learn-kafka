import os

import pytest

from app import create_app, db
from app.config import Config
from app.models import User, Registration # Added Registration


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use in-memory SQLite for tests
    SECRET_KEY = "test_secret_key"
    JWT_SECRET_KEY = "test_jwt_secret_key"
    WTF_CSRF_ENABLED = (
        False  # Disable CSRF for testing forms if any; useful for unit tests
    )
    # LOGIN_DISABLED = True # Removed as it may interfere with @login_required testing


@pytest.fixture(scope="session")
def app():
    """Session-wide test Flask application."""
    # Override FLASK_ENV using an environment variable for the test session
    # This ensures that create_app() sees FLASK_ENV=testing
    os.environ["FLASK_ENV"] = "testing"  # Ensure this is set before create_app

    app = create_app(config_class=TestConfig)  # Pass test config directly

    with app.app_context():
        db.create_all()  # Create database tables for in-memory db
        yield app  # Provide the app object to the tests
        db.drop_all()  # Drop all tables after the tests are done
        # db.session.remove() # Let test-specific sessions handle removal/rollback


@pytest.fixture(scope="function")
def db_session(app):
    """Ensures each test runs within a transaction that is rolled back."""
    with app.app_context():
        # Start a new SAVEPOINT, allowing rollback to this state
        # This uses the existing session provided by Flask-SQLAlchemy
        db.session.begin_nested()

        yield db.session

        # Rollback to the state before the SAVEPOINT
        db.session.rollback()
        # db.session.remove() # Not strictly necessary here as Flask-SQLAlchemy handles session scoping


@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture()
def test_user(db_session): # db_session is now Flask-SQLAlchemy's session in a nested transaction
    """Fixture to create a test user and save it to the database."""

    existing_user = User.query.filter_by(email="test@example.com").first() # Uses db_session implicitly
    if existing_user:
        # Manually delete associated registrations first
        registrations = Registration.query.filter_by(user_id=existing_user.id).all()
        for reg in registrations:
            db_session.delete(reg)
        db_session.delete(existing_user)
        db_session.flush()

    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture()
def auth_headers(client, test_user):
    """Fixture to get JWT token for a test user and return auth headers."""
    login_data = {"email": test_user.email, "password": "password123"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.get_json().get("access_token")
    return {"Authorization": f"Bearer {token}"}
