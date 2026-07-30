"""Models de domínio: Conversation e Message (Pydantic, sem lógica de negócio)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: str
    sender: Literal["user", "ai"]
    content: str
    created_at: datetime


class Conversation(BaseModel):
    id: str
    created_at: datetime
    messages: list[Message] = Field(default_factory=list)
