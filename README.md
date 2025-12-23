# Async Task Processor

Async Task Processor is a distributed background job processing system built using FastAPI, RabbitMQ, and PostgreSQL. It enables asynchronous execution of long-running tasks such as email sending and data processing using a producer-consumer architecture.

## Features
- Asynchronous task execution
- Reliable message delivery using RabbitMQ
- Scalable worker processes
- Retry mechanism for failed tasks
- Dead-letter queue handling
- Task status tracking in PostgreSQL
- Dockerized setup for easy deployment

## Architecture
```
Client -> FastAPI (Producer) -> RabbitMQ Queue -> Worker Services -> PostgreSQL
```

## Tech Stack
- Language: Python
- API Framework: FastAPI
- Message Broker: RabbitMQ
- Database: PostgreSQL
- Containerization: Docker, Docker Compose

## Setup Instructions
1. Install Docker and Docker Compose
2. Clone the repository
3. Run `docker compose up --build`
4. Access API at http://localhost:8000
5. RabbitMQ dashboard at http://localhost:15672

## Example API
POST /tasks
```
{
  "task_type": "send_email",
  "payload": {
    "to": "user@example.com"
  }
}
```