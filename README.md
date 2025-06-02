# Cricket Training Registration API

## Description
A Flask-based API for managing cricket training registrations. Users can register, log in, and then register for specific cricket training programs. The API uses JWT for secure authentication.

## Features
- User registration and login (email/password)
- JWT-based authentication for API endpoints
- Create and view cricket training registrations
- Database management with Flask-SQLAlchemy and Flask-Migrate
- Unit tests with pytest

## Technologies Used
- Python
- Flask
  - Flask-SQLAlchemy
  - Flask-Migrate
  - Flask-Login
  - Flask-JWT-Extended
- Werkzeug (for password hashing)
- pytest (for testing)
- python-dotenv (for environment variable management)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Copy the example `.env.example` file (if one exists, otherwise create `.env` directly) to `.env`:
        ```bash
        cp .env.example .env 
        ```
        If `.env.example` doesn't exist, create `.env` and add the following (replace with your actual secret keys and desired database URI):
        ```env
        FLASK_APP=run.py
        FLASK_ENV=development
        # For SQLite (creates app.db in the instance folder or project root based on config)
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db' 
        # Example for PostgreSQL:
        # SQLALCHEMY_DATABASE_URI='postgresql://user:password@host:port/dbname'
        SECRET_KEY='your_flask_secret_key_here' # Used for session management by Flask-Login
        JWT_SECRET_KEY='your_jwt_secret_key_here' # Used for JWTs
        ```
    *   **Important:** Generate strong random strings for `SECRET_KEY` and `JWT_SECRET_KEY`.

5.  **Run database migrations:**
    ```bash
    flask db upgrade
    ```
    (If you encounter issues with `flask` command not found after activating venv, you might need to use `python -m flask db upgrade`)

## Running the Application
To start the Flask development server:
```bash
python run.py
```
The API will typically be available at `http://127.0.0.1:5000/`.

## API Endpoints

All request and response bodies are in JSON format.

### Authentication

**1. User Registration**
*   **Endpoint:** `POST /auth/register_user`
*   **Description:** Registers a new user.
*   **Request Body:**
    ```json
    {
        "username": "newuser",
        "email": "user@example.com",
        "password": "securepassword123"
    }
    ```
*   **Success Response (201 CREATED):** 
    The actual response for registration in the current implementation is:
    ```json
    {
        "message": "User registered successfully"
    }
    ```
    To include user details, the route would need modification. For now, documenting as implemented.
*   **Error Response (409 CONFLICT - e.g., user already exists):**
    ```json
    {
        "message": "Username already exists" 
    }
    ```
    or
    ```json
    {
        "message": "Email already exists"
    }
    ```
*   **Error Response (400 BAD REQUEST - missing fields):**
    ```json
    {
        "message": "Missing username, email, or password"
    }
    ```

**2. User Login**
*   **Endpoint:** `POST /auth/login`
*   **Description:** Logs in an existing user and returns a JWT access token.
*   **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Login successful",
        "access_token": "<jwt_access_token>"
    }
    ```
*   **Error Response (401 UNAUTHORIZED):**
    ```json
    {
        "message": "Invalid email or password"
    }
    ```

**3. User Logout**
*   **Endpoint:** `POST /auth/logout`
*   **Description:** Logs out the currently authenticated user (session-based, requires `@login_required`).
*   **Authentication:** Requires session cookie from login (Flask-Login).
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Logout successful"
    }
    ```
*   **Error Response (401 UNAUTHORIZED - if not logged in):**
    (Flask-Login will return a 401 response by default for AJAX requests if not authenticated)

### Training Registrations

**Authentication:** These endpoints require a JWT Bearer token in the `Authorization` header.
`Authorization: Bearer <jwt_access_token>`

**1. Create Training Registration**
*   **Endpoint:** `POST /registrations`
*   **Description:** Creates a new training registration for the authenticated user.
*   **Request Body:**
    ```json
    {
        "sport": "cricket",
        "training_level": "intermediate"
    }
    ```
*   **Success Response (201 CREATED):**
    ```json
    {
        "message": "Registration successful", 
        "registration": {
            "id": 1,
            "user_id": 1,
            "sport": "cricket",
            "training_level": "intermediate",
            "registration_date": "YYYY-MM-DDTHH:MM:SS.ffffff" 
        }
    }
    ```
*   **Error Response (400 BAD REQUEST - e.g., missing fields):**
    ```json
    {
        "message": "Missing sport or training_level"
    }
    ```
*   **Error Response (401 UNAUTHORIZED - no/invalid JWT):**
    This can manifest in a few ways depending on the exact JWT error:
    ```json
    {
        "msg": "Missing Authorization Header" 
    } 
    ``` 
    or 
    ```json
    {
        "msg": "Token has expired"
    }
    ```
    or for other invalid token issues (e.g. malformed):
    ```json
    {
        "msg": "Invalid header padding" 
    }
    ```


**2. Get Training Registrations**
*   **Endpoint:** `GET /registrations`
*   **Description:** Retrieves all training registrations for the authenticated user.
*   **Success Response (200 OK):**
    An array of registration objects:
    ```json
    [
        {
            "id": 1,
            "user_id": 1,
            "sport": "cricket",
            "training_level": "intermediate",
            "registration_date": "YYYY-MM-DDTHH:MM:SS.ffffff"
        }
        // ... other registrations
    ]
    ```
*   **Error Response (401 UNAUTHORIZED - no/invalid JWT):**
    (Similar to create registration JWT errors)

## Running Tests
To run the unit tests:
```bash
pytest
```
Ensure your `pytest.ini` is configured, especially if your test database or environment variables differ from the defaults provided in the project. Also ensure `TestConfig` in `tests/conftest.py` is set up for your testing environment.
