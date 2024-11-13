from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg


class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str
    is_completed: Optional[bool] = Field(default=False)
    resources: Optional[str]
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
