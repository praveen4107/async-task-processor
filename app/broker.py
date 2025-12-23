import redis
import json
import uuid
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB, MAIN_QUEUE, DLQ, DELAYED_QUEUE

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def enqueue_task(task_name: str, args: dict, task_id: str = None, delay: int = 0):
    task_id = task_id or str(uuid.uuid.uuid4())
    payload = {
        "id": task_id,
        "task": task_name,
        "args": args,
        "retries": 0
    }
    serialized = json.dumps(payload)
    
    if delay > 0:
        score = delay + int(__import__('time').time())
        r.zadd(DELAYED_QUEUE, {serialized: score})
    else:
        r.lpush(MAIN_QUEUE, serialized)
    return task_id

def move_to_dlq(payload: str):
    r.lpush(DLQ, payload)

def requeue_with_delay(payload: dict, retry_count: int):
    backoff = BASE_BACKOFF * (2 ** retry_count)
    score = backoff + int(__import__('time').time())
    payload["retries"] = retry_count + 1
    r.zadd(DELAYED_QUEUE, {json.dumps(payload): score})