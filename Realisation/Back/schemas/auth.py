from pydantic import BaseModel
from typing import Optional

class AuthRequest(BaseModel):
    login: str
    password: str

class AuthResponse(BaseModel):
    result: str 
    role : Optional[str] = None # None если result="fail" или ошибка
    