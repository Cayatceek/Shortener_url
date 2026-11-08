# URL Shortener

Небольшой REST API для сокращения ссылок на FastAPI и SQLite. Создаёт короткие идентификаторы, сохраняет исходные адреса и перенаправляет пользователей.

## API

| Метод | Путь | Назначение |
| --- | --- | --- |
| POST | `/` | Создать короткую ссылку |
| GET | `/{short_id}` | Перенаправить на исходный URL (307) |
| GET | `/async-data` | Демонстрационный запрос к JSONPlaceholder |
| GET | `/docs` | Swagger UI |

Неизвестный идентификатор возвращает 404.

## Запуск через Docker

Создайте локальный файл `app/.env`:

```env
DB_PATH=/app/db/urls.db
```

Затем:

```bash
docker compose up --build
```

API: `http://127.0.0.1:8080`. SQLite хранится в именованном томе `url_data`.

Остановка:

```bash
docker compose down
```

## Запуск без Docker

```bash
python -m venv .venv
# Активируйте .venv
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Dockerfile использует Python 3.12. При запуске без Docker файл `.env` автоматически не загружается: задайте `DB_PATH` в окружении или используйте путь по умолчанию `app/urls.db`.

## Пример

```bash
curl -X POST http://127.0.0.1:8080/ \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Ответ содержит поле `short_url`. Откройте его, чтобы проверить перенаправление.

## Устройство проекта

- [app/router.py](app/router.py) — HTTP-маршруты.
- [app/services.py](app/services.py) — сокращение ссылок.
- [app/database.py](app/database.py) — SQLite и создание таблиц.
- [app/schemas.py](app/schemas.py) — схемы запросов и ответов.
- [docker-compose.yml](docker-compose.yml) — контейнер и постоянный том.

## Ограничения

Учебный сервис. Базовый адрес возвращаемых ссылок сейчас фиксирован как `http://127.0.0.1:8080`; перед размещением на домене его нужно сделать настраиваемым. В репозитории нет каталога автоматических тестов. Демонстрационный `/async-data` зависит от доступности внешнего API.

Условия использования: [LICENSE](LICENSE).
