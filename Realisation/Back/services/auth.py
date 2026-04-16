# Временная "база данных"
Users = {
    "admin": {"password": "secret123", "role": "admin"},
    "user1": {"password": "password", "role": "student"}
         }

def chek_auth(login: str, password: str) -> dict | None:
    """Проверяет логин и пароль пользователя.
    Возвращаем данные пользователя если всё ок, None если нет."""
  
    user = Users.get(login) # Ищем логин
    
    if user is None:
        return None  # Логин не найден
    
    if user["password"] != password:
        return None  # Пароль не верный
    
    return user
