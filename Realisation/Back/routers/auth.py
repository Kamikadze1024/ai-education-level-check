from fastapi import APIRouter
from schemas.auth import AuthRequest, AuthResponse
from services.auth import chek_auth
from fastapi import HTTPException


router = APIRouter()

@router.post("/auth", response_model=AuthResponse)
def authenticate(auth_request: AuthRequest) -> AuthResponse:
    if chek_auth(auth_request.login, auth_request.password):
        return AuthResponse(result="OK")
    
    else:
        raise HTTPException(status_code=401, detail="Fail:Неверный логин или пароль")
    
        