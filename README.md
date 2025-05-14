# URL Shortener API

A simple URL shortening service built with **FastAPI** and **SQLite**, containerized using **Docker**. The API allows users to shorten URLs, redirect to original URLs via short IDs, and access API documentation through an HTML page.

## Tech Stack
  - FastAPI for the API framework.
  - SQLite for persistent storage.
  - Docker for containerization.
  - Tailwind CSS for styling the `/docs` page.

## Features
- **Shorten URLs**: Create a short URL from a long one using `POST /`.
- **Redirect**: Redirect to the original URL using `GET /{short_id}`.
- **API Documentation**: View HTML-based API documentation at `GET /docs`.
- **Asynchronous**: Built with async/await for high performance.
- **Containerized**: Runs in Docker for easy deployment.
- **Tested**: Includes automated tests using `pytest`.

## Prerequisites
- **Docker Desktop**: Installed and running on your system.
- **Windows Subsystem for Linux (WSL 2)**: Required for Docker on Windows.
- **PowerShell**: For running commands on Windows.
- **Python 3.9** (optional): Only if running tests locally without Docker.

## Installation

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd Shortener_url
   ```

2. **Ensure Docker Desktop is Running**:
   - Open Docker Desktop and verify it's active in the system tray.
   - Check Docker version:
     ```powershell
     docker --version
     ```

3. **Verify WSL 2**:
   ```powershell
   wsl --list --all
   ```
   If WSL 2 is not installed, run:
   ```powershell
   wsl --install
   ```

## Project Structure
```
Shortener_url/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application setup
│   ├── router.py       # API routes (POST /, GET /{short_id}, GET /docs)
│   ├── services.py     # Business logic for URL shortening
│   ├── database.py     # SQLite database connection
│   ├── schemas.py      # Pydantic models for request/response
│   ├── models.py       # Data models for URLs
│   └── .env            # Environment variables (APP_PORT=8080)
├── tests/
│   ├── __init__.py
│   └── test_url.py     # Automated tests for API endpoints
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Running the Application

1. **Navigate to Project Directory**:
   ```powershell
   cd Shortener_url
   ```

2. **Build and Run with Docker Compose**:
   ```powershell
   docker-compose up --build
   ```
   - This builds the Docker image and starts the container.
   - The API will be available at `http://127.0.0.1:8080`.

3. **Stop the Application**:
   Press `Ctrl+C` in PowerShell, then:
   ```powershell
   docker-compose down
   ```

## API Endpoints

### POST /
Creates a shortened URL.

- **Request**:
  ```bash
  curl -X POST "http://127.0.0.1:8080/" -H "Content-Type: application/json" -d '{"url": "http://example.com"}'
  ```
- **Response** (201 Created):
  ```json
  {
    "short_url": "http://127.0.0.1:8080/<short_id>"
  }
  ```

### GET /{short_id}
Redirects to the original URL.

- **Request**:
  ```bash
  curl -L "http://127.0.0.1:8080/<short_id>"
  ```
- **Response** (307 Temporary Redirect):
  - Header: `Location: <original_url>`

### GET /docs
Returns an HTML page with API documentation.

- **Request**:
  ```bash
  curl "http://127.0.0.1:8080/docs"
  ```
- **Response** (200 OK):
  - HTML page styled with Tailwind CSS.
  - Open `http://127.0.0.1:8080/docs` in a browser for a better view.


### Manual Testing with PowerShell
1. **POST /**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8080/" -Method Post -ContentType "application/json" -Body '{"url": "http://example.com"}'
   ```

2. **GET /<short_id>**:
   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:8080/<short_id>" -MaximumRedirection 0
   ```

3. **GET /docs**:
   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:8080/docs"
   ```

## Troubleshooting

- **Error: `no such table: urls`**:
  - Ensure `app/main.py` calls `init_db()` on startup.
  - Check `urls.db`:
    ```powershell
    docker exec -it url_shortener bash
    sqlite3 /app/urls.db
    .tables
    ```

- **Error: `GET /docs` returns 404`**:
  - Verify `app/router.py` has `@router.get("/docs")` before `@router.get("/{short_id}")`.
  - Rebuild:
    ```powershell
    docker-compose down
    docker rmi url_shortener
    docker-compose up --build
    ```

- **Orphan Containers Warning**:
  - Remove old containers:
    ```powershell
    docker rm shortener_url-web-1
    ```

- **Network Issues**:
  - Verify Docker Desktop and WSL 2:
    ```powershell
    docker ps
    wsl --list --all
    ```
