# 🧠 НейроЭкзаменатор — Фронтенд

## Структура проекта

```
Front/
├── main.py                       ← точка входа, запускать отсюда
│
├── views/
│   ├── __init__.py
│   ├── auth_view.py              ← страница входа (форма логин/пароль)
│   └── main_view.py              ← главная страница (заглушка)
│
├── backend/
│   ├── __init__.py
│   └── backend_client.py         ← ВСЕ HTTP-вызовы к бэкенду здесь
│
├── theme/
│   ├── __init__.py
│   └── global_styles.py          ← CSS тёмной темы
│
├── requirements.txt
└── README.md
```

> ⚠️ Папка называется `views/`, а не `pages/` —  
> `pages/` зарезервирована Streamlit и вызывает ошибку импорта.

---

## Запуск

```bash
# 1. Установить зависимости (один раз)
pip install -r requirements.txt

# 2. Запустить
streamlit run main.py
```

Приложение откроется на `http://localhost:8501`

---

## 🔌 Ручки интеграции с бэкендом

Все вызовы к бэкенду — в файле **`backend/backend_client.py`**.

### Сменить адрес бэкенда

```python
# backend/backend_client.py, строка 1
BACKEND_URL = "http://localhost:8000"   # ← сюда вписать нужный адрес
```

---

### POST /auth — аутентификация

```
POST {BACKEND_URL}/auth
Content-Type: application/json

{"login": "ivanov", "password": "secret"}
```

| Результат | HTTP-статус | Тело ответа |
|-----------|-------------|-------------|
| Успех     | `200`       | `{"status": "OK"}` |
| Ошибка    | `401 / 403` | любое |

При успехе фронт переходит на главную страницу.  
При любом другом статусе — показывает сообщение об ошибке.

---

### Добавить новый вызов бэкенда

Добавьте функцию в `backend/backend_client.py`:

```python
def get_questions(exam_id: int) -> dict:
    """GET {BACKEND_URL}/exams/{exam_id}/questions"""
    response = requests.get(f"{BACKEND_URL}/exams/{exam_id}/questions",
                            timeout=REQUEST_TIMEOUT)
    ...
```

---

### Добавить новую страницу

1. Создайте `views/my_view.py` с функцией `render()`
2. В `main.py` добавьте импорт и условие:

```python
from views.my_view import render as render_my

if st.session_state.get("page") == "my":
    render_my()
```
