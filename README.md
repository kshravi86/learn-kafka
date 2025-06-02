# FastAPI Student CRUD and Auth API

## Description

This project is a FastAPI-based application that provides a RESTful API for managing student data. It includes functionalities for student registration, login, and CRUD (Create, Read, Update, Delete) operations on student records.

The application uses an in-memory dictionary as a temporary database. Password hashing is implemented for security.

## Requirements

*   Python 3.7+
*   FastAPI
*   Uvicorn
*   Passlib (for password hashing)
*   python-multipart (for form data in login)
*   email-validator (for Pydantic email validation)
*   pytest (for running tests)

All dependencies are listed in `requirements.txt`.

## How to Install Dependencies

1.  Clone the repository (if you haven't already).
2.  Navigate to the project's root directory.
3.  It's recommended to create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

1.  Ensure all dependencies are installed.
2.  Navigate to the project's root directory.
3.  Run the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    *   `--reload`: Enables auto-reloading when code changes (useful for development).
    *   `--host 0.0.0.0`: Makes the server accessible on your network.
    *   `--port 8000`: Specifies the port to run on. You can change this if needed.

The API will then be accessible at `http://localhost:8000` (or `http://<your-ip>:8000`). API documentation (Swagger UI) will be available at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

## Available Endpoints

### Authentication
*   **`POST /register`**: Register a new student.
    *   **Request Body**: `{"username": "str", "email": "EmailStr", "password": "str", "full_name": "Optional[str]"}`
    *   **Response (201 Created)**: `{"username": "str", "email": "EmailStr", "full_name": "Optional[str]"}` (password is not returned)
    *   **Error Responses**: 409 Conflict (username already exists), 422 Unprocessable Entity (validation error).
*   **`POST /login`**: Log in an existing student.
    *   **Request Body (form data)**: `username=your_username&password=your_password`
    *   **Response (200 OK)**: `{"message": "Login successful", "username": "str"}` (placeholder, token can be added here)
    *   **Error Responses**: 401 Unauthorized (incorrect credentials).

### Student Management
*   **`GET /students/{username}`**: Get details for a specific student.
    *   **Response (200 OK)**: `{"username": "str", "email": "EmailStr", "full_name": "Optional[str]"}`
    *   **Error Responses**: 404 Not Found.
*   **`PUT /students/{username}`**: Update details for a specific student.
    *   **Request Body**: `{"email": "Optional[EmailStr]", "full_name": "Optional[str]"}`
    *   **Response (200 OK)**: `{"username": "str", "email": "EmailStr", "full_name": "Optional[str]"}`
    *   **Error Responses**: 404 Not Found, 422 Unprocessable Entity (validation error).
*   **`DELETE /students/{username}`**: Delete a specific student.
    *   **Response (200 OK)**: `{"message": "Student deleted successfully"}`
    *   **Error Responses**: 404 Not Found.

## How to Run Tests

1.  Ensure all dependencies, including `pytest`, are installed.
2.  Navigate to the project's root directory.
3.  Run pytest:
    ```bash
    pytest
    ```
    This will discover and run all tests in the `tests` directory.
