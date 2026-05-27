from pydantic import BaseModel
from typing import Optional


class AuthRequest(BaseModel):
    login: str  # логин пользователя
    password: str  # пароль пользователя


class AuthResponse(BaseModel):
    result: str  # результат аутентификации: "OK" / "Fail" / "Error"
    # роль пользователя: "admin" / "student" / None если не прошёл
    role: Optional[str] = None
