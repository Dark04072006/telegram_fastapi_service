from typing import Optional

from pydantic import BaseModel


class MessageSchema(BaseModel):
    role: str
    content: str


class UserSchema(BaseModel):
    user_id: int
    messages: Optional[list[MessageSchema]] = None
    is_subscriber: Optional[bool] = None


class UserUpdateSchema(BaseModel):
    messages: Optional[list[MessageSchema]] = None
    is_subscriber: bool


class LoginSchema(BaseModel):
    username: str
    password: str
