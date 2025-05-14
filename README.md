# URL Shortener Service

This is an HTTP service built with FastAPI for shortening URLs and performing async requests.

## Setup

1. Install Docker and Docker Compose.
2. Clone the repository.
3. Run:
   ```bash
   docker-compose up --build
   ```

## Endpoints

- **POST /**: Shorten a URL.  
  Example:
  ```bash
  curl -X POST "http://127.0.0.1:8080/" -H "Content-Type: application/json" -d '{"url": "http://example.com"}'
  ```

- **GET /<short_id>**: Redirect to the original URL.  
  Example:
  ```bash
  curl -L "http://127.0.0.1:8080/<short_id>"
  ```

- **GET /async-data**: Fetch data from an external API.  
  Example:
  ```bash
  curl "http://127.0.0.1:8080/async-data"
  ```

## Testing

Run tests with:
```bash
pytest tests/test_url.py -v
```