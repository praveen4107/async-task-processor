from fastapi import FastAPI
from pydantic import BaseModel
from app.producer import enqueue

app = FastAPI(title="Async Task Processor API")

class TaskRequest(BaseModel):
    task: str
    args: dict = {}

@app.post("/enqueue")
def api_enqueue(req: TaskRequest):
    task_id = enqueue(req.task, req.args)
    return {"task_id": task_id, "status": "enqueued"}