from sqlmodel import SQLModel, Field
from sqlalchemy import text

from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    question = "question"
    answer = "answer"


class Message(SQLModel, table=True):
    id: int = Field(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    content: str
    type: MessageType = Field(index=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)")
        }
    )
    
    def to_html_data(self):
        return {
            "type": self.type.value,
            "content": self.content
        }
