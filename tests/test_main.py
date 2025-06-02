import sys
import os
from fastapi.testclient import TestClient

# Add project root to sys.path to allow importing 'main' and 'database'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app # Adjust if your app instance or main file is named differently
from database import fake_students_db # To clean up after tests

client = TestClient(app)

def setup_function():
    # Clear the fake_students_db before each test function to ensure test isolation
    fake_students_db.clear()

# It's good practice to use test functions that start with 'test_'
# --- Registration Tests ---
def test_register_student_success():
    setup_function() # Call setup manually if not using a test runner that supports it automatically
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123", "full_name": "Test User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "hashed_password" not in data # Ensure StudentDisplay model is working

def test_register_student_duplicate_username():
    setup_function()
    # First registration
    client.post("/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    # Attempt to register again with the same username
    response = client.post("/register", json={"username": "testuser", "email": "test2@example.com", "password": "password456"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already registered"

def test_register_student_invalid_email():
    setup_function()
    response = client.post(
        "/register",
        json={"username": "anotheruser", "email": "not-an-email", "password": "password123"}
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation errors

# --- Login Tests ---
def test_login_success():
    setup_function()
    # Register first
    client.post("/register", json={"username": "loginuser", "email": "login@example.com", "password": "password123", "full_name": "Login User"})
    response = client.post(
        "/login",
        data={"username": "loginuser", "password": "password123"} # OAuth2PasswordRequestForm uses form data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["username"] == "loginuser"


def test_login_incorrect_username():
    setup_function()
    response = client.post("/login", data={"username": "nonexistentuser", "password": "password123"})
    assert response.status_code == 401

def test_login_incorrect_password():
    setup_function()
    client.post("/register", json={"username": "loginuser2", "email": "login2@example.com", "password": "correctpassword"})
    response = client.post("/login", data={"username": "loginuser2", "password": "wrongpassword"})
    assert response.status_code == 401

# --- Get Student Tests ---
def test_get_student_details_success():
    setup_function()
    client.post("/register", json={"username": "getuser", "email": "get@example.com", "password": "password", "full_name": "Get User"})
    response = client.get("/students/getuser")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "getuser"
    assert data["email"] == "get@example.com"

def test_get_student_details_not_found():
    setup_function()
    response = client.get("/students/nosuchuser")
    assert response.status_code == 404

# --- Update Student Tests ---
def test_update_student_details_success():
    setup_function()
    client.post("/register", json={"username": "updateuser", "email": "update@example.com", "password": "password", "full_name": "Update User"})
    response = client.put(
        "/students/updateuser",
        json={"email": "updated@example.com", "full_name": "Updated Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["full_name"] == "Updated Name"

def test_update_student_details_not_found():
    setup_function()
    response = client.put("/students/nosuchuserupdate", json={"email": "new@example.com"})
    assert response.status_code == 404

# --- Delete Student Tests ---
def test_delete_student_success():
    setup_function()
    client.post("/register", json={"username": "deleteuser", "email": "delete@example.com", "password": "password"})
    response = client.delete("/students/deleteuser")
    assert response.status_code == 200 # Based on current plan
    assert response.json()["message"] == "Student deleted successfully"
    
    # Verify student is actually deleted
    get_response = client.get("/students/deleteuser")
    assert get_response.status_code == 404

def test_delete_student_not_found():
    setup_function()
    response = client.delete("/students/nosuchuserdelete")
    assert response.status_code == 404
