# URL Shortener API 🌟

Welcome to the **URL Shortener API**! 🎉 A simple, lightning-fast service built with **FastAPI** and **SQLite**, wrapped in a **Docker** container. Shrink those long URLs, redirect like a pro, and fetch data from external APIs asynchronously. 

## Tech Stack 🛠️
- **FastAPI**: Blazing-fast API framework with async magic. ⚡
- **SQLite**: Lightweight, reliable database for storing URLs. 💾
- **Docker**: Containerized for easy setup and deployment. 🐳
- **httpx**: Async HTTP client for fetching external data. 🌐

## Features 🎯
- **Shrink URLs**: Turn long links into short ones with `POST /`. 🔗
- **Redirect**: Jump to the original URL using `GET /{short_id}`. 🏃‍♂️
- **Async Data Fetch**: Grab data from an external API with `GET /async-data`. 📡
- **Dockerized**: Deploy anywhere with a single command. 🐳

## Prerequisites 📋
- **Docker Desktop**: Get it running on your machine! 🖥️
- **Windows Subsystem for Linux (WSL 2)**: Needed for Docker on Windows. 🐧
- **PowerShell**: For running commands like a boss. 💪
- **Python 3.9** (optional): Only if you want to tinker locally. 🐍

## Quick Start ⚡
1. **Clone the Repository** (if you have it):
   ```bash
   git clone <repository-url>
   cd Shortener_url
   ```

2. **Check Docker Desktop**:
   - Make sure it's running (look for the whale in the system tray! 🐳).
   - Verify version:
     ```powershell
     docker --version
     ```

3. **Confirm WSL 2**:
   ```powershell
   wsl --list --all
   ```
   Not installed? No sweat, run:
   ```powershell
   wsl --install
   ```

4. **Run the App**:
   ```powershell
   cd C:\Users\user\Desktop\test_tesk\Shortener_url
   docker-compose up --build
   ```
   - Boom! API is live at `http://127.0.0.1:8080`. 🌍

5. **Stop the App**:
   Hit `Ctrl+C` in PowerShell, then:
   ```powershell
   docker-compose down
   ```

## Project Structure 📂
```
Shortener_url/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app setup 🎮
│   ├── router.py       # API routes (POST /, GET /{short_id}, GET /async-data) 🚦
│   ├── services.py     # URL shortening logic 🛠️
│   ├── database.py     # SQLite connection 🔌
│   ├── schemas.py      # Pydantic models for requests/responses 📋
│   ├── models.py       # URL data models 📊
│   └── .env            # Environment variables (APP_PORT=8080) 🔑
├── tests/
│   ├── __init__.py
│   └── test_url.py     # Automated tests for endpoints 🧪
├── Dockerfile          # Docker image config 🐳
├── docker-compose.yml  # Docker Compose setup ⚙️
├── requirements.txt    # Python dependencies 📦
├── .gitignore          # Git ignore file 🙈
├── LICENSE             # MIT License 📜
└── README.md           # You're reading it! 😄
```

## API Endpoints 🌐

### POST / 🔗
Creates a shiny new shortened URL.

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

### GET /{short_id} 🏃‍♂️
Redirects to the original URL.

- **Request**:
  ```bash
  curl -L "http://127.0.0.1:8080/<short_id>"
  ```
- **Response** (307 Temporary Redirect):
  - Header: `Location: <original_url>`

### GET /async-data 📡
Fetches data from an external API (JSONPlaceholder) asynchronously. Cool, right? 😎

- **Request**:
  ```bash
  curl "http://127.0.0.1:8080/async-data"
  ```
- **Response** (200 OK):
  ```json
  {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
  }
  ```

## Try It Out! 🕹️
Test the API with PowerShell commands:

1. **POST /**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8080/" -Method Post -ContentType "application/json" -Body '{"url": "http://example.com"}'
   ```

2. **GET /<short_id>**:
   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:8080/<short_id>" -MaximumRedirection 0
   ```

3. **GET /async-data**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8080/async-data"
   ```

## Troubleshooting 🛠️
- **Error: `no such table: urls`**:
  - Check if `app/main.py` calls `init_db()`.
  - Inspect `urls.db`:
    ```powershell
    docker exec -it url_shortener bash
    sqlite3 /app/urls.db
    .tables
    ```

- **Error: `/async-data` returns 500**:
  - Test network:
    ```powershell
    docker exec url_shortener curl https://jsonplaceholder.typicode.com/todos/1
    ```
  - Verify `httpx`:
    ```powershell
    docker exec url_shortener pip show httpx
    ```

- **Orphan Containers Warning**:
  - Clean up:
    ```powershell
    docker rm shortener_url-web-1
    ```

- **Network Issues**:
  - Check Docker Desktop and WSL 2:
    ```powershell
    docker ps
    wsl --list --all
    ```
  - Update WSL:
    ```powershell
    wsl --update
    ```
