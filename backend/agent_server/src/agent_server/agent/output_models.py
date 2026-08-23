from pydantic import BaseModel

class EmailValidationResponse(BaseModel):
    is_valid: bool = False
    message: str