from pydantic import BaseModel

class MessageQuestion(BaseModel):
    question: str
    
class MessageAnswer(BaseModel):
    content: str
    type: str