from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import status as http_status

from .crud import DocumentCRUD
from .dependencies import get_document_crud
from api.dependencies import get_llm
from .models import Document

router = APIRouter()

@router.post(
   "",
   response_model=Document,
   status_code=http_status.HTTP_201_CREATED
)
async def create_document(
   file: UploadFile = File(...),
   documents: DocumentCRUD = Depends(get_document_crud),
   llm = Depends(get_llm)
):
   document = await documents.create(file=file)
   await llm.update_content()
   return document


@router.get(
   "/{document_id}",
   response_model=Document,
   status_code=http_status.HTTP_200_OK
)
async def get_document_by_id(
   document_id: int,
   documents: DocumentCRUD = Depends(get_document_crud)
):
   document = await documents.retrieve(document_id=document_id)
   return document


@router.get(
   "",
   response_model=list[Document],
   status_code=http_status.HTTP_200_OK
)
async def get_document_list(
   documents: DocumentCRUD = Depends(get_document_crud)
):
   documents = await documents.list()
   return documents


@router.delete(
   "/{document_id}",
   status_code=http_status.HTTP_200_OK
)
async def delete_document(
   document_id: int,
   documents: DocumentCRUD = Depends(get_document_crud)
):
   status = await documents.delete(document_id=document_id)
   return {"status": status, "message": "The document has been deleted!"}