from fastapi import APIRouter
from schemas.auth import AuthRequest, AuthResponse
from services.auth import chek_auth



router = APIRouter()

@router.post("/auth", response_model=AuthResponse)
def authenticate(auth_request: AuthRequest) -> AuthResponse:
    try:
        user=chek_auth(auth_request.login, auth_request.password)
        
        if user is None:
            return AuthResponse(result="Fail. Аутентификация не пройдена")
                                
        return AuthResponse(result="OK", role=user["role"])
        
       
    except Exception:
        return AuthResponse(result="Error, что-то пошло не так...", role=None)  # "Oops, что-то пошло не так..."
    
    
        