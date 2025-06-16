from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import status as http_status

from .crud import MessageCRUD
from .dependencies import get_message_crud
from .models import Message, MessageType
from .schemas import MessageAnswer, MessageQuestion
from api.dependencies import get_llm

router = APIRouter()

@router.post(
   "/ask",
   response_model=MessageAnswer,
   status_code=http_status.HTTP_201_CREATED
)
async def ask_question(
   body: MessageQuestion,
   messages: MessageCRUD = Depends(get_message_crud),
   llm = Depends(get_llm)
):
   message = await messages.create(
      content=body.question,
      type=MessageType.question
   )
   answer = llm.generate_answer(message.content)
   message = await messages.create(
      content=answer,
      type=MessageType.answer
   )
   return {
      "content": message.content,
      "type": message.type.value
   }


@router.get(
   "",
   response_model=list[Message],
   status_code=http_status.HTTP_200_OK
)
async def get_messages_list(
   messages: MessageCRUD = Depends(get_message_crud),
):
    return await messages.list()
