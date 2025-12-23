FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY api ./api  # If using API

ENV PYTHONUNBUFFERED=1

# Default command – override in compose/k8s
CMD ["python", "-m", "app.worker"]