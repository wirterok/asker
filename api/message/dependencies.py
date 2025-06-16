from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from asker.db import get_async_session
from api.message.crud import MessageCRUD


async def get_message_crud(
    session: AsyncSession = Depends(get_async_session)
) -> MessageCRUD:
       return MessageCRUD(session=session)
