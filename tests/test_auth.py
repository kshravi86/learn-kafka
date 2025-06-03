import pytest  # noqa: F401

from app.models import User


def test_register_user_success(client):
    """Test successful user registration."""
    response = client.post(
        "/auth/register_user",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"
    assert User.query.filter_by(email="new@example.com").first() is not None


def test_register_user_existing_username(client, test_user):
    """Test registration with an existing username."""
    response = client.post(
        "/auth/register_user",
        json={
            "username": test_user.username,  # Existing username
            "email": "another@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 409
    assert response.get_json()["message"] == "Username already exists"


def test_register_user_existing_email(client, test_user):
    """Test registration with an existing email."""
    response = client.post(
        "/auth/register_user",
        json={
            "username": "anotheruser",
            "email": test_user.email,  # Existing email
            "password": "password123",
        },
    )
    assert response.status_code == 409
    assert response.get_json()["message"] == "Email already exists"


def test_register_user_missing_fields(client):
    """Test registration with missing fields."""
    response = client.post(
        "/auth/register_user",
        json={
            "username": "missingfielduser"
            # Missing email and password
        },
    )
    assert response.status_code == 400
    assert (
        response.get_json()["message"] == "Missing username, email, or password"
    )  # Adjust if message is more specific


def test_login_success(client, test_user):
    """Test successful user login and JWT token generation."""
    response = client.post(
        "/auth/login",
        json={
            "email": test_user.email,
            "password": "password123",  # Correct password for test_user
        },
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Login successful"
    assert "access_token" in json_data


def test_login_incorrect_password(client, test_user):
    """Test login with incorrect password."""
    response = client.post(
        "/auth/login", json={"email": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid email or password"


def test_login_nonexistent_user(client):
    """Test login with a non-existent email."""
    response = client.post(
        "/auth/login", json={"email": "nouser@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid email or password"


def test_logout_success(client, auth_headers):
    """Test successful logout."""
    # Flask-Login's logout_user doesn't interact with JWTs in this stateless auth setup.
    # /logout uses session-based Flask-Login via @login_required.
    # For pure JWT, /logout might invalidate a token (denylist) or be client-side.
    # Test if endpoint is reachable & returns success with a session.
    # auth_headers provide JWT, not a session cookie for @login_required.
    # Test might need adjustment based on @login_required's JWT interaction.
    # If @login_required is strictly for session auth, this test would fail (401).
    # Assuming it's a simple endpoint that should return success.
    # If protected by @jwt_required(), auth_headers would be used.

    # For a stateless JWT logout, the client is responsible for discarding the token.
    # The server endpoint is informational.
    response = client.post("/auth/logout")  # No specific headers needed

    assert response.status_code == 200
    assert response.get_json()["message"] == (
        "Logout successful. Please discard your JWT token on the client-side."
    )
