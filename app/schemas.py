from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

Priority = Literal["low", "medium", "high"]


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
    created_at: datetime
    updated_at: datetime
