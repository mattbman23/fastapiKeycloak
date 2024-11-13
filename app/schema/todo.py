from pydantic import BaseModel
from typing import Optional


class TodoCreateSchema(BaseModel):
    task: str
    is_completed: Optional[bool] = None
