# 🧠 НейроЭкзаменатор — Фронтенд

Фронтенд-часть системы оценки знаний на **Streamlit (Python)**.

---

## Структура проекта

```
Front/
├── main.py                    # Точка входа. Маршрутизация: auth → main
│
├── pages/
│   ├── auth_page.py           # Страница аутентификации (форма входа)
│   └── main_page.py           # Главная страница (заглушка)
│
├── api/
│   └── backend_client.py      # Слой работы с бэкендом (все HTTP-вызовы здесь)
│
├── styles/
│   └── global_styles.py       # Глобальные CSS-стили тёмной темы
│
├── requirements.txt           # Зависимости Python
└── README.md                  # Этот файл
```

---

## Запуск проекта

### 1. Установить зависимости

```bash
cd Front
pip install -r requirements.txt
```

### 2. Запустить фронтенд

```bash
streamlit run main.py
```
python main.py

По умолчанию приложение откроется на `http://localhost:8501`.

### 3. Опциональные параметры запуска

```bash
# Другой порт
streamlit run main.py --server.port 8502

# Отключить автоматическое открытие браузера
streamlit run main.py --server.headless true
```

---

## 🔌 Ручки интеграции с бэкендом

> Все вызовы к бэкенду сосредоточены в одном файле:  
> **`backend/backend_client.py`**

### Настройка адреса бэкенда

Откройте `backend/backend_client.py` и измените переменную:

```python
BACKEND_URL = "http://localhost:8000"   # ← сюда вписать адрес вашего бэкенда
```

---

### Эндпоинт 1 — Аутентификация

| Поле     | Значение                        |
|----------|---------------------------------|
| Метод    | `POST`                          |
| URL      | `{BACKEND_URL}/auth`            |
| Тело     | `{"login": str, "password": str}` |

**Пример запроса:**
```json
POST http://localhost:8000/auth
Content-Type: application/json

{
  "login": "ivanov",
  "password": "secret123"
}
```

**Ожидаемый ответ при успехе (HTTP 200):**
```json
{
  "status": "OK"
}
```

**При ошибке — любой другой HTTP-статус** (401, 403, 500 и т.д.).  
Фронт покажет пользователю сообщение об ошибке.

---

## Логика переходов между страницами

```
Открытие приложения
        │
        ▼
authenticated == False?
   ├─ Да  → показать auth_page.py (форма входа)
   │          │
   │          └─ нажата кнопка «Войти»
   │                │
   │                └─ POST /auth
   │                      ├─ 200 OK  → authenticated = True → main_page
   │                      └─ ошибка  → показать сообщение об ошибке
   │
   └─ Нет → показать main_page.py (главная страница)
                │
                └─ нажата кнопка «Выйти» → authenticated = False → auth_page
```

---

## Как добавить новые страницы

1. Создайте файл в `pages/`, например `pages/exam_page.py`, с функцией `render()`.
2. В `main.py` добавьте импорт и условие маршрутизации.

```python
from pages.exam_page import render as render_exam

if st.session_state.get("current_page") == "exam":
    render_exam()
```

---

## Как добавить новые вызовы бэкенда

Добавьте новую функцию в `backend/backend_client.py`:

```python
def get_questions(exam_id: int) -> dict:
    """
    GET {BACKEND_URL}/exams/{exam_id}/questions
    Возвращает список вопросов для экзамена.
    """
    url = f"{BACKEND_URL}/exams/{exam_id}/questions"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    ...
```

---

## Требования

- Python 3.9+
- Streamlit 1.32+
- Доступ к интернету (для загрузки Google Fonts)
