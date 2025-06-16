
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from asker.db import get_async_session
from api.documents.crud import DocumentCRUD


async def get_document_crud(
       session: AsyncSession = Depends(get_async_session)
) -> DocumentCRUD:
       return DocumentCRUD(session=session)