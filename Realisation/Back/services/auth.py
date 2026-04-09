# Временная "база данных"
Users = {
    "admin": "admin123",    
    "user1": "password1",
    "user2": "password2"
}

def chek_auth(login: str, password: str) -> bool:
    """Проверяет логин и пароль пользователя."""
    user_password = Users.get(login) # Ищем логин
    
    if user_password is None:
        return False
    
    return user_password == password  # Сравниваем пароли

    