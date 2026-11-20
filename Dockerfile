FROM python:3.11-slim

WORKDIR /code

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic.ini .
COPY migrations ./migrations

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
