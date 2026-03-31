"""
backend/backend_client.py — Все вызовы к бэкенду в одном месте.

Чтобы сменить адрес бэкенда — измените переменную BACKEND_URL.

══════════════════════════════════════════════
🔌 РУЧКИ ДЛЯ ИНТЕГРАЦИИ С БЭКЕНДОМ:
══════════════════════════════════════════════

1. Аутентификация
   Метод : POST
   URL   : {BACKEND_URL}/auth
   Body  : {"login": "<str>", "password": "<str>"}
   Успех : HTTP 200, {"status": "OK"}
   Ошибка: любой другой HTTP-статус

══════════════════════════════════════════════
"""

import requests

# ── Адрес бэкенда — меняйте здесь ─────────────────────────────
BACKEND_URL = "http://localhost:8000"

# Таймаут ожидания ответа (секунды)
REQUEST_TIMEOUT = 10


def authenticate(login: str, password: str) -> dict:
    """
    POST {BACKEND_URL}/auth
    Body: {"login": str, "password": str}

    Возвращает:
        {"success": True,  "message": ""}           — вход разрешён
        {"success": False, "message": "<причина>"}  — вход отклонён
    """
    url = f"{BACKEND_URL}/auth"
    payload = {"login": login, "password": password}

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return {"success": True, "message": ""}
            # 200, но тело не совпадает с ожидаемым
            return {"success": False, "message": data.get("message", "Неверный ответ сервера.")}

        if response.status_code in (401, 403):
            return {"success": False, "message": "Неверный логин или пароль."}

        return {"success": False, "message": f"Ошибка сервера: HTTP {response.status_code}."}

    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд."}

    except requests.exceptions.Timeout:
        return {"success": False, "message": f"Сервер не ответил за {REQUEST_TIMEOUT} секунд."}

    except Exception as e:
        return {"success": False, "message": f"Неожиданная ошибка: {e}"}
