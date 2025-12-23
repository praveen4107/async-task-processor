# async-task-processor

A **production-ready distributed task queue** built in Python. Demonstrates key system design concepts: scalability, fault tolerance, retries, dead-letter queues, and horizontal scaling.

Inspired by Celery/RQ/BullMQ, but simpler

## Features

-   Async task enqueuing (with optional delays)
-   Exponential backoff retries
-   Dead-letter queue for permanent failures
-   Idempotent tasks (unique IDs)
-   Horizontal worker scaling
-   Redis-backed persistence
-   Optional FastAPI HTTP endpoint
-   Dockerized + Kubernetes-ready

## Tech Stack

-   Python 3.12
-   Redis
-   FastAPI + Uvicorn
-   Docker & Docker Compose
-   Kubernetes

## Architecture

```
[Client / API] → Enqueue → Redis (Broker)
                             ↓
                 [Multiple Workers] ← Poll & Execute
                             ↓
           Success → Done    Failure → Retry → DLQ
```

## Quick Start (Docker Compose)

```
git clone https://github.com/yourusername/async-task-processor.git
cd async-task-processor
docker compose up --build
```

### Enqueue via Python

```
from app.producer import enqueue
enqueue("send_email", {"to": "user@example.com", "subject": "Hello"})
```

### Enqueue via API

```
curl -X POST http://localhost:8000/enqueue\
  -H "Content-Type: application/json"\
  -d '{"task": "process_image", "args": {"url": "https://example.com/img.jpg"}}'
```

## Production Deployment (Kubernetes)

```
docker build -t yourusername/async-task-processor:latest .
docker build -f api/Dockerfile -t yourusername/async-task-processor-api:latest .
docker push yourusername/async-task-processor:latest
docker push yourusername/async-task-processor-api:latest

kubectl apply -f k8s/
```

Scale workers:

```
kubectl scale deployment/atp-worker --replicas=20
```

