from pydantic import BaseModel
from typing import Dict
from uuid import UUID

class TaskRequest(BaseModel):
    task_type: str
    payload: Dict
