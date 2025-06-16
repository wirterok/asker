import os, shutil, uuid

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Message, MessageType


class MessageCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, content: str, type: MessageType) -> Message:
        record = Message(
            content=content,
            type=type
        )

        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record
    
    async def list(self) -> list[Message]:
        statement = select(Message)
        results = await self.session.exec(statement=statement)
        messages = results.scalars()
        return messages
