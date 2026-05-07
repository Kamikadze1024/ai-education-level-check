from fastapi import APIRouter
from schemas.auth import AuthRequest, AuthResponse
from services.auth import chek_auth

router = APIRouter(prefix="/core")  # все роуты этого файла начинаются с /core


# обрабатываем POST /core/auth
@router.post("/auth", response_model=AuthResponse)
def authenticate(auth_request: AuthRequest) -> AuthResponse:
    try:
        # вызываем сервис проверки логина и пароля
        user = chek_auth(auth_request.login, auth_request.password)

        if user is None:
            # пользователь не найден или пароль неверный
            return AuthResponse(result="Fail. Аутентификация не пройдена")

        # аутентификация успешна — возвращаем роль пользователя
        return AuthResponse(result="OK", role=user["role"])

    except Exception:
        # непредвиденная ошибка
        # "Oops, что-то пошло не так..."
        return AuthResponse(result="Error, что-то пошло не так...", role=None)
