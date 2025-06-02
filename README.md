# Bus Ticketing Django App

## Description
This project is a Django application that provides CRUD (Create, Read, Update, Delete) operations for a bus ticketing system. It allows managing bus routes, schedules, and pricing. The application is containerized using Docker and includes a GitHub Actions workflow for CI/CD to build and push Docker images to Docker Hub.

## Features
- List all available buses.
- View details of a specific bus.
- Add new bus entries (name, source, destination, departure/arrival times, price).
- Update existing bus entries.
- Delete bus entries.

## Technology Stack
- **Backend**: Python, Django
- **WSGI Server**: Gunicorn
- **Database**: SQLite (default Django DB, can be configured for others)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Prerequisites
- Python 3.9+
- Pip (Python package installer)
- Docker (for running the application in a container)
- Git (for cloning the repository)

## Local Setup & Running

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Navigate to the Django project directory:**
    ```bash
    cd bus_ticketing_project
    ```

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be accessible at `http://127.0.0.1:8000/ticketing/`.

## Running with Docker

1.  **Build the Docker image:**
    From the project root directory (where the `Dockerfile` is located):
    ```bash
    docker build -t bus-ticketing-app .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 bus-ticketing-app
    ```
    The application will be accessible at `http://localhost:8000/ticketing/`.

## Running Tests
To run the automated tests for the `ticketing` app:
```bash
# Ensure you are in the bus_ticketing_project directory
python manage.py test ticketing
```

## CI/CD (Deployment)
This project uses GitHub Actions for CI/CD. A workflow is configured in `.github/workflows/docker-publish.yml` to:
- Automatically build a Docker image on pushes to the `main` branch.
- Push the built image to Docker Hub.

**Note**: For the workflow to successfully push to Docker Hub, the following secrets must be configured in the GitHub repository settings (`Settings > Secrets and variables > Actions`):
- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: Your Docker Hub access token.
