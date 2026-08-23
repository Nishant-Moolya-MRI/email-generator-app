from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class SendMailRequest(BaseModel):
    sender_mail: EmailStr
    receiver_mail: EmailStr
    mail_content: str

class SendMailResponse(BaseModel):
    message: str
    status: Literal["success", "error"]

class GenerateMailRequest(BaseModel):
    email_tone: str
    data_points: str
    additional_description: Optional[str] = ""
    
class GenerateMailResponse(BaseModel):
    subject: str
    body_content: str
