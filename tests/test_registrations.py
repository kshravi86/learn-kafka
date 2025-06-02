import pytest
from app.models import Registration, db
from datetime import datetime

def test_create_registration_success(client, test_user, auth_headers):
    """Test successful creation of a new registration."""
    response = client.post('/registrations', json={
        'sport': 'cricket',
        'training_level': 'beginner'
    }, headers=auth_headers)
    
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['message'] == 'Registration successful'
    assert 'registration' in json_data
    assert json_data['registration']['sport'] == 'cricket'
    assert json_data['registration']['training_level'] == 'beginner'
    assert json_data['registration']['user_id'] == test_user.id
    
    # Verify in DB
    reg = Registration.query.filter_by(user_id=test_user.id, sport='cricket').first()
    assert reg is not None
    assert reg.training_level == 'beginner'

def test_create_registration_no_token(client):
    """Test creating registration without JWT token."""
    response = client.post('/registrations', json={
        'sport': 'cricket',
        'training_level': 'beginner'
    }) # No headers
    assert response.status_code == 401 # Expecting 'Missing Authorization Header' or similar by Flask-JWT-Extended

def test_create_registration_invalid_token(client):
    """Test creating registration with an invalid/expired JWT token."""
    response = client.post('/registrations', json={
        'sport': 'cricket',
        'training_level': 'beginner'
    }, headers={'Authorization': 'Bearer invalidtoken'})
    assert response.status_code == 422 # Flask-JWT-Extended: "Invalid header padding" or other errors

def test_create_registration_missing_fields(client, auth_headers):
    """Test creating registration with missing sport or training_level."""
    response_missing_sport = client.post('/registrations', json={
        'training_level': 'beginner'
        # Missing sport
    }, headers=auth_headers)
    assert response_missing_sport.status_code == 400
    assert response_missing_sport.get_json()['message'] == 'Missing sport or training_level'

    response_missing_level = client.post('/registrations', json={
        'sport': 'cricket'
        # Missing training_level
    }, headers=auth_headers)
    assert response_missing_level.status_code == 400
    assert response_missing_level.get_json()['message'] == 'Missing sport or training_level'

def test_get_registrations_success(client, test_user, auth_headers):
    """Test successful retrieval of user's registrations."""
    # Create a couple of registrations for the test_user
    with client.application.app_context():
        reg1 = Registration(user_id=test_user.id, sport='cricket', training_level='beginner', registration_date=datetime.utcnow())
        reg2 = Registration(user_id=test_user.id, sport='football', training_level='intermediate', registration_date=datetime.utcnow())
        db.session.add_all([reg1, reg2])
        db.session.commit()

    response = client.get('/registrations', headers=auth_headers)
    assert response.status_code == 200
    registrations_data = response.get_json()
    assert isinstance(registrations_data, list)
    assert len(registrations_data) == 2
    
    sports_retrieved = {reg['sport'] for reg in registrations_data}
    assert 'cricket' in sports_retrieved
    assert 'football' in sports_retrieved
    for reg_data in registrations_data:
        assert reg_data['user_id'] == test_user.id

def test_get_registrations_no_token(client):
    """Test retrieving registrations without JWT token."""
    response = client.get('/registrations') # No headers
    assert response.status_code == 401

def test_get_registrations_other_user(client, app, auth_headers):
    """Test that a user cannot see registrations of another user."""
    # auth_headers are for test_user
    
    # Create another user and a registration for them
    with app.app_context():
        other_user = User(username='otheruser', email='other@example.com')
        other_user.set_password('password123')
        db.session.add(other_user)
        db.session.commit()
        
        # At this point other_user.id will be populated
        other_reg = Registration(user_id=other_user.id, sport='tennis', training_level='advanced')
        db.session.add(other_reg)
        db.session.commit()

    response = client.get('/registrations', headers=auth_headers)
    assert response.status_code == 200
    registrations_data = response.get_json()
    assert isinstance(registrations_data, list)
    # Should only contain registrations of test_user (which is 0 in this specific test if not pre-added by other tests in the same session)
    # or any registrations added for test_user within this test or by its fixtures.
    # Crucially, it should NOT contain 'tennis'.
    for reg_data in registrations_data:
        assert reg_data['sport'] != 'tennis'
        assert reg_data['user_id'] != other_user.id
    
    # To be more precise, let's ensure it's empty if test_user has no registrations
    # Clean up any registrations for test_user first for a clean state for this specific check
    # Get test_user_id from the app context as test_user fixture might be out of scope or less direct
    with app.app_context():
        test_user_instance = User.query.filter_by(email='test@example.com').first()
        assert test_user_instance is not None, "Test user not found in database for cleanup"
        test_user_id = test_user_instance.id
        
        Registration.query.filter_by(user_id=test_user_id).delete()
        db.session.commit()
        
    response_clean = client.get('/registrations', headers=auth_headers)
    assert response_clean.status_code == 200
    assert response_clean.get_json() == []
