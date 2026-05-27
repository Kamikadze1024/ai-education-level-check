# AI EdTech Exam — Frontend

Корпоративная платформа для тестирования знаний.  
Frontend на Python (Flask + pywebview), подключается к бэкенду на `localhost:8000`.

---

## Стек

| Слой | Технология |
|------|-----------|
| UI-обёртка | pywebview 5 (нативное окно) |
| Веб-сервер | Flask 3 (локальный прокси) |
| Стили | CSS Custom Properties, тёмная/светлая тема |
| Иконки | Phosphor Icons (CDN) |
| Шрифты | Syne + DM Sans (Google Fonts) |
| Логика | Vanilla JS ES2022 (SPA) |

---

## Структура проекта

```
ai_edtech_exam/
├── main.py              # Точка входа — запускает Flask + pywebview
├── app.py               # Flask application factory
├── routes.py            # HTTP-маршруты, прокси к бэкенду
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   │   └── main.css     # Все стили
│   └── js/
│       └── app.js       # SPA-логика
└── templates/
    └── index.html       # HTML-оболочка
```

---

## Быстрый старт

### 1. Убедитесь, что бэкенд запущен

```bash
# Бэкенд должен быть доступен на http://localhost:8000
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

> **Windows**: для pywebview может потребоваться `pip install pywebview[cef]`  
> **Linux**: потребуется `pip install pywebview[gtk]` и пакеты `python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0`  
> **macOS**: работает из коробки через WebKit

### 4. Запустите приложение

```bash
python main.py
```

Откроется нативное окно 1440×900.

---

## Запуск только браузерной версии (без pywebview)

Если pywebview не нужен, можно запустить Flask напрямую и открыть в браузере:

```bash
python -c "from app import create_app; create_app().run(port=5050, debug=True)"
# затем откройте http://127.0.0.1:5050
```

---

## Настройка адреса бэкенда

Адрес бэкенда задаётся в `routes.py`:

```python
BACKEND_URL = "http://localhost:8000"
```

---

## Функциональность

### Авторизация
- Поле логина, пароля с show/hide
- Чекбокс «Запомнить меня» (сохраняет в localStorage)
- Обработка: `fail`, `admin`, `student`, недоступный сервер

### Администратор
1. **Загрузка базы знаний** — drag&drop / выбор файла, progress bar, PDF/TXT/DOC/DOCX
2. **Генерация вопросов** — spinbox'ы (кол-во вопросов, ответов, правильных)
3. **Просмотр вопросов** — карточки с правильными/неправильными ответами, кнопка сохранения

### Студент
1. **Список экзаменов** — таблица с radio-кнопками
2. **Прохождение экзамена** — чекбоксы ответов, отправка, результат

---

## UI-особенности
- Тёмная и светлая тема (сохраняется в localStorage)
- Toast-уведомления (4 типа)
- Modal-окна с анимацией
- Loading-screen при запуске
- Адаптация под FullHD (1440px)
- Плавные CSS-анимации везде
