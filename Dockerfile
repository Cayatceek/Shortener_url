FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc musl-dev linux-headers

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]