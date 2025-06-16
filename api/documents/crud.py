import os, shutil, uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import TextExtractor
from .models import Document
from asker import settings

UPLOAD_DIR = f"{settings.base_dir}/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.text_extractor = TextExtractor()
    
    async def create(self, file: UploadFile) -> Document:
        if not (file.content_type.startswith("application/pdf")
            or file.content_type.startswith("text/")
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF or text files are supported"
            )

        unique_name = str(uuid.uuid4()).split('-')[0]
        unique_name = f"{unique_name}_{file.filename}"
        save_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            extracted_text = self.text_extractor.extract_text_from_file(
                save_path, file.content_type
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to extract text: {str(e)}"
            )

        record = Document(
            filename=unique_name,
            content_type=file.content_type,
            size=os.path.getsize(save_path),
            path=save_path,
            content=extracted_text,
        )

        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record
    
    async def list(self) -> list[Document]:
        statement = select(Document)
        results = await self.session.exec(statement=statement)
        documents = results.scalars()
        return documents
    
    async def retrieve(self, document_id: int) -> Document:
        statement = select(Document).where(
            Document.id == document_id
        )
        results = await self.session.exec(statement=statement)
        document = results.scalar_one_or_none()

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The document hasn't been found!"
            )

        return document

    async def delete(self, document_id) -> bool:
        path = (await self.retrieve(document_id)).path
        statement = delete(Document).where(
            Document.id == document_id
        )

        await self.session.exec(statement=statement)
        await self.session.commit()
        os.remove(path)
        return 200
