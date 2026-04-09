from pydantic import BaseModel

class AuthRequest(BaseModel):
    login: str
    password: str

class AuthResponse(BaseModel):
    result: str 

    