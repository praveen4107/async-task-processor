from .broker import enqueue_task

def enqueue(task_name: str, args: dict = None, task_id: str = None):
    return enqueue_task(task_name, args or {}, task_id)