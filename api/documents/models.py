from sqlmodel import SQLModel, Field
from sqlalchemy import text

from datetime import datetime


class Document(SQLModel, table=True):
    id: int = Field(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    filename: str
    content_type: str
    size: int
    path: str
    content: str
    uploaded_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)")
        } 
    )
