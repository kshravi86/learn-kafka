import pytest
from app.models import User, db

def test_register_user_success(client):
    """Test successful user registration."""
    response = client.post('/auth/register_user', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'
    assert User.query.filter_by(email='new@example.com').first() is not None

def test_register_user_existing_username(client, test_user):
    """Test registration with an existing username."""
    response = client.post('/auth/register_user', json={
        'username': test_user.username, # Existing username
        'email': 'another@example.com',
        'password': 'password123'
    })
    assert response.status_code == 409
    assert response.get_json()['message'] == 'Username already exists'

def test_register_user_existing_email(client, test_user):
    """Test registration with an existing email."""
    response = client.post('/auth/register_user', json={
        'username': 'anotheruser',
        'email': test_user.email, # Existing email
        'password': 'password123'
    })
    assert response.status_code == 409
    assert response.get_json()['message'] == 'Email already exists'

def test_register_user_missing_fields(client):
    """Test registration with missing fields."""
    response = client.post('/auth/register_user', json={
        'username': 'missingfielduser'
        # Missing email and password
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Missing username, email, or password' # Adjust if message is more specific

def test_login_success(client, test_user):
    """Test successful user login and JWT token generation."""
    response = client.post('/auth/login', json={
        'email': test_user.email,
        'password': 'password123' # Correct password for test_user
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Login successful'
    assert 'access_token' in json_data

def test_login_incorrect_password(client, test_user):
    """Test login with incorrect password."""
    response = client.post('/auth/login', json={
        'email': test_user.email,
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid email or password'

def test_login_nonexistent_user(client):
    """Test login with a non-existent email."""
    response = client.post('/auth/login', json={
        'email': 'nouser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid email or password'

def test_logout_success(client, auth_headers):
    """Test successful logout."""
    # Flask-Login's logout_user doesn't really interact with JWT tokens in this setup for stateless auth.
    # The @login_required on /logout in auth_routes.py uses session-based Flask-Login.
    # For a pure JWT setup, /logout might invalidate a token if using a denylist, or just be a client-side action.
    # Here, we test if the endpoint is reachable and returns success with a valid session (if login_user was called).
    # However, our auth_headers provide JWT, not a session cookie for @login_required.
    # This test might need adjustment based on how @login_required is intended to work with JWT.
    # If @login_required is strictly for session auth, this test will fail with 401 without a session.
    # Let's assume for now it's a simple endpoint that should return success if called.
    # If it were protected by @jwt_required(), auth_headers would be used.
    
    # To make this test pass with current setup where /logout uses Flask-Login's @login_required:
    # 1. Log in first to create a session
    client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password123'})
    # 2. Then call logout
    response = client.post('/auth/logout') # No auth_headers needed if it relies on session
    
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Logout successful'

def test_logout_requires_login(client):
    """Test that logout requires login (fails if no session)."""
    response = client.post('/auth/logout') # Call without logging in
    assert response.status_code == 401 # Expect redirect to login or 401 by Flask-Login
                                      # Flask-Login typically redirects to login_manager.login_view
                                      # If login_view is not set up to handle AJAX or returns HTML,
                                      # the status might be different or check for redirect.
                                      # For APIs, a 401 is more common.
                                      # In our __init__.py, login_manager.login_view = 'auth.login'
                                      # Flask-Login's default unauthorized handler returns 401.
                                      
                                      
# To make the test_logout_requires_login more robust for an API context:
# If Flask-Login redirects, the status code might be 302.
# If it returns 401 directly (common for APIs), then 401 is correct.
# The default behavior of Flask-Login when @login_required fails is to call `unauthorized()`
# which by default aborts with 401. So 401 is expected.
