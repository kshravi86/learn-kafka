from datetime import datetime

import pytest # noqa: F401

from app.models import Registration, User # Ensure User is imported if used directly
# Assuming db is imported from app or app.models if direct db operations are needed
# For instance, if tests interact with db.session directly for setup/assertions.
# from app import db # Or from app.models import db, depending on project structure.
# The conftest.py db_session fixture manages db.session within tests.


# Scenario 2a: Test Successful Registration Creation (Covered by existing test_create_registration_success)
def test_create_registration_success(client, test_user, auth_headers, db_session): # Added db_session for explicitness
    """Test successful creation of a new registration."""
    response = client.post(
        "/registrations",
        json={"sport": "cricket", "training_level": "beginner"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Registration successful"
    assert "registration" in json_data
    assert json_data["registration"]["sport"] == "cricket"
    assert json_data["registration"]["training_level"] == "beginner"
    assert json_data["registration"]["user_id"] == test_user.id

    # Verify in DB using the test-specific session
    reg = db_session.query(Registration).filter_by(user_id=test_user.id, sport="cricket").first()
    assert reg is not None
    assert reg.training_level == "beginner"


# Scenario 2b: Test Registration Creation with Missing Fields (Covered by existing test_create_registration_missing_fields)
def test_create_registration_missing_fields(client, auth_headers):
    """Test creating registration with missing sport or training_level."""
    # Test missing sport
    response_missing_sport = client.post(
        "/registrations",
        json={"training_level": "beginner"}, # Missing sport
        headers=auth_headers,
    )
    assert response_missing_sport.status_code == 400
    assert response_missing_sport.get_json()["message"] == "Missing sport or training_level"

    # Test missing training_level
    response_missing_level = client.post(
        "/registrations",
        json={"sport": "cricket"}, # Missing training_level
        headers=auth_headers,
    )
    assert response_missing_level.status_code == 400
    assert response_missing_level.get_json()["message"] == "Missing sport or training_level"


# Scenario 2c: Test Registration Creation without JWT Token (Covered by existing test_create_registration_no_token)
def test_create_registration_no_token(client):
    """Test creating registration without JWT token."""
    response = client.post(
        "/registrations", json={"sport": "cricket", "training_level": "beginner"}
    )  # No headers
    assert response.status_code == 401
    # Flask-JWT-Extended default message for missing token is "Missing Authorization Header"
    # or similar based on its configuration.
    # assert "Missing Authorization Header" in response.get_json().get("msg", "")


# Scenario 2d: Test Registration Creation with Invalid/Expired JWT Token (Covered by existing test_create_registration_invalid_token)
def test_create_registration_invalid_token(client):
    """Test creating registration with an invalid/expired JWT token."""
    response = client.post(
        "/registrations",
        json={"sport": "cricket", "training_level": "beginner"},
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 422  # Flask-JWT-Extended error for invalid token format/content


# Scenario 2e: Test Successful Retrieval of Registrations (Covered and enhanced from existing test_get_registrations_success)
def test_get_registrations_success(client, test_user, auth_headers, db_session): # Added db_session
    """Test successful retrieval of user's registrations."""
    # Create a couple of registrations for the test_user
    reg1 = Registration(
        user_id=test_user.id,
        sport="cricket",
        training_level="beginner",
        registration_date=datetime.utcnow(),
    )
    reg2 = Registration(
        user_id=test_user.id,
        sport="football",
        training_level="intermediate",
        registration_date=datetime.utcnow(),
    )
    db_session.add_all([reg1, reg2])
    db_session.flush() # Use flush as commit is handled by db_session rollback

    response = client.get("/registrations", headers=auth_headers)
    assert response.status_code == 200
    registrations_data = response.get_json()
    assert isinstance(registrations_data, list)
    assert len(registrations_data) == 2

    sports_retrieved = {reg["sport"] for reg in registrations_data}
    assert "cricket" in sports_retrieved
    assert "football" in sports_retrieved
    for reg_data in registrations_data:
        assert reg_data["user_id"] == test_user.id


# Scenario 2f: Test Retrieval of Registrations for a User with No Registrations (New Test)
def test_get_registrations_for_user_with_no_registrations(client, test_user, auth_headers, db_session):
    """Test retrieving registrations for a user who has none."""
    # Ensure no registrations for test_user (db_session ensures clean state from other tests)
    # For absolute certainty within this test, one could delete any existing ones,
    # but db_session rollback should handle this.
    registrations = db_session.query(Registration).filter_by(user_id=test_user.id).all()
    assert len(registrations) == 0, "Test setup error: User should have no registrations at start of this test."

    response = client.get("/registrations", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json() == []


# Scenario 2g: Test Retrieval of Registrations without JWT Token (Covered by existing test_get_registrations_no_token)
def test_get_registrations_no_token(client):
    """Test retrieving registrations without JWT token."""
    response = client.get("/registrations")  # No headers
    assert response.status_code == 401
    # Similar to 2c, check for Flask-JWT-Extended's specific message if needed.
    # assert "Missing Authorization Header" in response.get_json().get("msg", "")

# This existing test is valuable for authorization logic.
def test_get_registrations_other_user(client, app, auth_headers, db_session, test_user): # Added db_session and test_user
    """Test that a user cannot see registrations of another user."""
    # auth_headers are for test_user

    # Create another user and a registration for them
    other_user = User(username="otheruser", email="other@example.com")
    other_user.set_password("password123")
    db_session.add(other_user)
    db_session.flush() # Flush to get other_user.id

    other_reg = Registration(
        user_id=other_user.id, sport="tennis", training_level="advanced"
    )
    db_session.add(other_reg)
    db_session.flush()

    # Ensure test_user has no registrations before making the call
    # This makes the assertion at the end cleaner.
    existing_test_user_regs = db_session.query(Registration).filter_by(user_id=test_user.id).all()
    for reg in existing_test_user_regs:
        db_session.delete(reg)
    db_session.flush()

    response = client.get("/registrations", headers=auth_headers)
    assert response.status_code == 200
    registrations_data = response.get_json()
    assert isinstance(registrations_data, list)
    # Should only contain registrations of test_user, which is 0 for this specific check.
    assert len(registrations_data) == 0, "test_user should have no registrations visible to them in this check"

    # Double check that no registrations from other_user are present
    for reg_data in registrations_data:
        assert reg_data["sport"] != "tennis"
        assert reg_data["user_id"] != other_user.id
