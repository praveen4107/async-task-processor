from fastapi import FastAPI
from uuid import uuid4
from models import TaskRequest
from queue import publish_task
from database import get_db

app = FastAPI(title="Async Task Processor")

@app.post("/tasks")
def create_task(task: TaskRequest):
    task_id = str(uuid4())

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO tasks (id, task_type, payload, status) VALUES (%s, %s, %s, %s)",
        (task_id, task.task_type, task.payload, "PENDING"),
    )
    db.commit()
    cur.close()
    db.close()

    publish_task({
        "id": task_id,
        "task_type": task.task_type,
        "payload": task.payload,
        "retries": 0
    })

    return {"task_id": task_id, "status": "queued"}
