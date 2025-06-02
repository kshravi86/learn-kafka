import pytest
from app import create_app, db
from app.models import User
from app.config import Config
import os

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory SQLite for tests
    SECRET_KEY = 'test_secret_key'
    JWT_SECRET_KEY = 'test_jwt_secret_key'
    WTF_CSRF_ENABLED = False # Disable CSRF for testing forms if any; useful for unit tests
    # LOGIN_DISABLED = True # Removed as it may interfere with @login_required testing

@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application."""
    # Override FLASK_ENV using an environment variable for the test session
    # This ensures that create_app() sees FLASK_ENV=testing
    os.environ['FLASK_ENV'] = 'testing' # Ensure this is set before create_app
    
    app = create_app(config_class=TestConfig) # Pass test config directly
    
    with app.app_context():
        db.create_all() # Create database tables for in-memory db
        yield app # Provide the app object to the tests
        db.drop_all() # Drop all tables after the tests are done
        db.session.remove() # Ensure session is closed

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture()
def test_user(app):
    """Fixture to create a test user and save it to the database."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture()
def auth_headers(client, test_user):
    """Fixture to get JWT token for a test user and return auth headers."""
    login_data = {
        'email': test_user.email,
        'password': 'password123'
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    token = response.get_json().get('access_token')
    return {'Authorization': f'Bearer {token}'}
