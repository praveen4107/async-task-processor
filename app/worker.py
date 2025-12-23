import json
import time
from redis import Redis
from .config import MAIN_QUEUE, DELAYED_QUEUE, DLQ, MAX_RETRIES
from .tasks import TASK_REGISTRY
from .broker import move_to_dlq

r = Redis(decode_responses=True)  # Reuse connection

def run_worker():
    print("Worker started – listening on queues...")
    while True:
        # Check delayed first
        now = int(time.time())
        delayed = r.zrangebyscore(DELAYED_QUEUE, 0, now, withscores=False)
        for item in delayed:
            r.lpush(MAIN_QUEUE, item)
            r.zrem(DELAYED_QUEUE, item)
        
        # Block pop from main queue
        payload_str = r.brpop(MAIN_QUEUE, timeout=10)
        if not payload_str:
            continue
        payload = json.loads(payload_str[1])
        
        task_func = TASK_REGISTRY.get(payload["task"])
        if not task_func:
            print(f"Unknown task {payload['task']}")
            continue
        
        try:
            task_func(**payload["args"])
            print(f"Success: {payload['id']} - {payload['task']}")
        except Exception as e:
            print(f"Failed: {payload['id']} - retry {payload['retries']}")
            if payload["retries"] >= MAX_RETRIES:
                move_to_dlq(payload_str[1])
                print(f"Moved to DLQ: {payload['id']}")
            else:
                from .broker import requeue_with_delay
                requeue_with_delay(payload, payload["retries"])