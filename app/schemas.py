from typing import Literal, Optional

from pydantic import BaseModel, Field

Priority = Literal["low", "medium", "high"]


class TodoCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[str] = None
    priority: Optional[Priority] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None
    priority: Optional[Priority] = None


class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[str]
    priority: Optional[Priority]
    created_at: str
    updated_at: str
