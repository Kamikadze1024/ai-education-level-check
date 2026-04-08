"""
backend/backend_client.py — Все вызовы к бэкенду в одном месте.

Чтобы сменить адрес бэкенда — измените переменную BACKEND_URL.

══════════════════════════════════════════════════════════════
🔌 РУЧКИ ДЛЯ ИНТЕГРАЦИИ С БЭКЕНДОМ:
══════════════════════════════════════════════════════════════

1. Аутентификация
   Метод : POST
   URL   : {BACKEND_URL}/auth
   Тело  : {"login": "<str>", "password": "<str>"}
   200 OK: {"status": "OK"}
   Ошибка: любой другой HTTP-статус

2. Генерация вопросов
   Метод : POST
   URL   : {BACKEND_URL}/generate
   Тело  : multipart/form-data
               files[]       — список файлов (PDF / TXT)
               num_questions — количество вопросов (int)
               num_answers   — количество правильных ответов (int)
   200 OK: {"status": "OK", "questions": [...]}
   Ошибка: любой другой HTTP-статус

══════════════════════════════════════════════════════════════

ДЕМО-РЕЖИМ (DEMO_MODE = True):
    Функция generate_questions() НЕ обращается к серверу.
    Она делает паузу 3 секунды (имитация работы модели)
    и возвращает успешный ответ-заглушку.
    Это позволяет проверить работу интерфейса без бэкенда.

    Чтобы подключить боевой бэкенд:
        1. Установите DEMO_MODE = False
        2. Убедитесь что бэкенд запущен на BACKEND_URL
"""

import time
import requests

# ── Адрес бэкенда — меняйте здесь ─────────────────────────────────────
BACKEND_URL = "http://localhost:8000"

# Таймаут ожидания ответа в секундах
REQUEST_TIMEOUT = 60   # для генерации вопросов нужно больше времени

# ══════════════════════════════════════════════════════════════════════
# ДЕМО-РЕЖИМ: True = работает без бэкенда (заглушка)
#             False = реальные запросы к серверу
# ══════════════════════════════════════════════════════════════════════
DEMO_MODE = True


# ──────────────────────────────────────────────────────────────────────
# 1. АУТЕНТИФИКАЦИЯ
# ──────────────────────────────────────────────────────────────────────

def authenticate(login: str, password: str) -> dict:
    """
    POST {BACKEND_URL}/auth
    Тело: {"login": str, "password": str}

    Возвращает:
        {"success": True,  "message": ""}
        {"success": False, "message": "<причина>"}
    """
    
    # ДЕМО: убрать когда бэкенд будет готов
    if DEMO_MODE:
        return {"success": True, "message": ""}
        
    url     = f"{BACKEND_URL}/auth"
    payload = {"login": login, "password": password}

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return {"success": True, "message": ""}
            return {"success": False, "message": data.get("message", "Неверный ответ сервера.")}

        if response.status_code in (401, 403):
            return {"success": False, "message": "Неверный логин или пароль."}

        return {"success": False, "message": f"Ошибка сервера: HTTP {response.status_code}."}

    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Не удалось подключиться к серверу."}

    except requests.exceptions.Timeout:
        return {"success": False, "message": f"Сервер не ответил за {REQUEST_TIMEOUT} секунд."}

    except Exception as e:
        return {"success": False, "message": f"Неожиданная ошибка: {e}"}


# ──────────────────────────────────────────────────────────────────────
# 2. ГЕНЕРАЦИЯ ВОПРОСОВ
# ──────────────────────────────────────────────────────────────────────

def generate_questions(files: list, num_questions: int, num_answers: int) -> dict:
    """
    POST {BACKEND_URL}/generate  (multipart/form-data)

    Параметры:
        files         — список объектов файлов из st.file_uploader
        num_questions — количество вопросов для генерации
        num_answers   — количество правильных ответов на один вопрос

    Возвращает:
        {"success": True,  "message": "Вопросы сформированы."}
        {"success": False, "message": "<причина ошибки>"}

    ──────────────────────────────────────────────
    ДЕМО-РЕЖИМ (DEMO_MODE = True):
        Реальный запрос НЕ отправляется.
        Функция делает паузу 3 сек и возвращает успех.
        Используйте для проверки интерфейса без бэкенда.
    ──────────────────────────────────────────────
    """

    # ── ДЕМО-РЕЖИМ ──────────────────────────────────────────────
    if DEMO_MODE:
        time.sleep(3)   # имитируем время работы языковой модели
        return {
            "success": True,
            "message": (
                f"Вопросы сформированы. "
                f"Создано {num_questions} вопросов "
                f"с {num_answers} правильным ответом на каждый. "
                f"(демо-режим — бэкенд не подключён)"
            ),
        }

    # ── БОЕВОЙ РЕЖИМ ────────────────────────────────────────────
    url = f"{BACKEND_URL}/generate"

    # Формируем список файлов для multipart-запроса.
    # Каждый элемент: ("files[]", (имя_файла, содержимое, тип_содержимого))
    files_payload = []
    for f in files:
        mime = "application/pdf" if f.name.endswith(".pdf") else "text/plain"
        files_payload.append(("files[]", (f.name, f.read(), mime)))

    # Дополнительные параметры передаём как поля формы
    data_payload = {
        "num_questions": str(num_questions),
        "num_answers":   str(num_answers),
    }

    try:
        response = requests.post(
            url,
            files=files_payload,
            data=data_payload,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return {"success": True, "message": "Вопросы сформированы."}
            return {"success": False, "message": data.get("message", "Неверный ответ сервера.")}

        return {"success": False, "message": f"Ошибка сервера: HTTP {response.status_code}."}

    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Не удалось подключиться к серверу."}

    except requests.exceptions.Timeout:
        return {"success": False, "message": "Сервер не ответил вовремя. Попробуйте снова."}

    except Exception as e:
        return {"success": False, "message": f"Неожиданная ошибка: {e}"}
