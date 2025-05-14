from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from .schemas import URLCreate, URLResponse
from .services import create_short_url, get_original_url
import httpx

router = APIRouter()

@router.get("/docs", response_class=HTMLResponse)
async def get_api_docs():
    """Возвращает HTML-страницу с документацией API.

    Returns:
        HTMLResponse: HTML-страница с описанием эндпоинтов API.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>URL Shortener API Documentation</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 font-sans">
        <div class="container mx-auto p-6 max-w-4xl">
            <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">URL Shortener API</h1>
            <p class="text-lg text-gray-600 mb-6">
                This API provides functionality to shorten URLs and redirect to original URLs using a short identifier.
            </p>

            <h2 class="text-2xl font-semibold text-gray-800 mt-8 mb-4">Endpoints</h2>

            <div class="bg-white p-6 rounded-lg shadow-md mb-6">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">POST /</h3>
                <p class="text-gray-600 mb-2">Creates a shortened URL.</p>
                <p class="text-gray-600 mb-2"><strong>Parameters:</strong></p>
                <ul class="list-disc pl-6 text-gray-600">
                    <li><code>url</code> (JSON body): The original URL to shorten (string).</li>
                </ul>
                <p class="text-gray-600 mb-2"><strong>Response:</strong></p>
                <pre class="bg-gray-100 p-4 rounded"><code>
{
  "short_url": "http://127.0.0.1:8080/&lt;short_id&gt;"
}
                </code></pre>
                <p class="text-gray-600 mb-2"><strong>Status Code:</strong> 201 Created</p>
                <p class="text-gray-600"><strong>Example:</strong></p>
                <pre class="bg-gray-100 p-4 rounded"><code>
curl -X POST "http://127.0.0.1:8080/" -H "Content-Type: application/json" -d '{"url": "http://example.com"}'
                </code></pre>
            </div>

            <div class="bg-white p-6 rounded-lg shadow-md mb-6">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">GET /&lt;short_id&gt;</h3>
                <p class="text-gray-600 mb-2">Redirects to the original URL associated with the short ID.</p>
                <p class="text-gray-600 mb-2"><strong>Parameters:</strong></p>
                <ul class="list-disc pl-6 text-gray-600">
                    <li><code>short_id</code> (path): The unique identifier of the shortened URL.</li>
                </ul>
                <p class="text-gray-600 mb-2"><strong>Response:</strong> Redirect to the original URL</p>
                <p class="text-gray-600 mb-2"><strong>Status Code:</strong> 307 Temporary Redirect</p>
                <p class="text-gray-600 mb-2"><strong>Headers:</strong></p>
                <ul class="list-disc pl-6 text-gray-600">
                    <li><code>Location</code>: The original URL</li>
                </ul>
                <p class="text-gray-600"><strong>Example:</strong></p>
                <pre class="bg-gray-100 p-4 rounded"><code>
curl -L "http://127.0.0.1:8080/abc123"
                </code></pre>
            </div>

            <div class="bg-white p-6 rounded-lg shadow-md mb-6">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">GET /docs</h3>
                <p class="text-gray-600 mb-2">Returns this API documentation page.</p>
                <p class="text-gray-600 mb-2"><strong>Parameters:</strong> None</p>
                <p class="text-gray-600 mb-2"><strong>Response:</strong> HTML page with API documentation</p>
                <p class="text-gray-600 mb-2"><strong>Status Code:</strong> 200 OK</p>
                <p class="text-gray-600"><strong>Example:</strong></p>
                <pre class="bg-gray-100 p-4 rounded"><code>
curl "http://127.0.0.1:8080/docs"
                </code></pre>
            </div>

            <footer class="text-center text-gray-600 mt-8">
                <p>Built with FastAPI and SQLite &copy; 2025</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

        
@router.post("/", response_model=URLResponse, status_code=201)
async def shorten_url(url: URLCreate):
    """Создаёт сокращённый URL.

    Args:
        url (URLCreate): Объект с оригинальным URL.

    Returns:
        URLResponse: Объект с сокращённым URL.
    """
    short_id = await create_short_url(url.url)
    short_url = f"http://127.0.0.1:8080/{short_id}"
    return URLResponse(short_url=short_url)

@router.get("/{short_id}")
async def redirect_to_original(short_id: str):
    """Перенаправляет на оригинальный URL по сокращённому идентификатору.

    Args:
        short_id (str): Уникальный идентификатор сокращённого URL.

    Returns:
        RedirectResponse: Перенаправление на оригинальный URL с кодом 307.

    Raises:
        HTTPException: Если URL не найден (код 404).
    """
    url_obj = await get_original_url(short_id)
    if url_obj is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_obj.original_url, status_code=307)