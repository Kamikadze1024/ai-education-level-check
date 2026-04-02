"""
main.py — Точка входа фронтенда нейроэкзаменатора.

pip install -r requirements.txt

python main.py




Логика маршрутизации:
    authenticated == False  →  страница входа  (views/auth_view.py)
    authenticated == True   →  главная страница (views/main_view.py)

Состояние сессии (st.session_state):
    authenticated (bool) — флаг успешного входа
    username      (str)  — логин вошедшего пользователя


"""


import sys
import os
import subprocess
import streamlit as st
from views.auth_view import render as render_auth    # страница входа
from views.main_view import render as render_main    # главная страница
from theme.global_styles import inject_styles        # тёмная CSS-тема


# Добавляем папку проекта в sys.path — чтобы Python находил
# пакеты views/, theme/, backend/ при любом способе запуска.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run():
    """
    Запускает Streamlit-сервер программно через subprocess.
    Вызывается при python main.py.
    Использует тот же интерпретатор Python, что и текущий процесс —
    это гарантирует корректную работу внутри virtualenv.
    """
   
 
    # sys.executable — путь к текущему python (в т.ч. внутри venv)
    # __file__       — абсолютный путь к этому файлу
    subprocess.run(
        [
            sys.executable,       # python из активного окружения
            "-m", "streamlit",    # запускаем streamlit как модуль
            "run",
            __file__,             # передаём этот же файл как приложение
            "--server.headless", "false",   # открывать браузер автоматически
        ],
        check=True,
    )
 
 


# set_page_config обязан быть первым вызовом Streamlit
st.set_page_config(
    page_title="AI EdTech Exam",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)



# Инициализация session_state при первом запуске
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Применяем глобальные стили
inject_styles()

# Маршрутизация
if st.session_state.authenticated:
    render_main()
else:
    render_auth()



if __name__ == "__main__" and os.environ.get("STREAMLIT_RUNNING") != "1":
  
 
    env = os.environ.copy()
    env["STREAMLIT_RUNNING"] = "1"   # флаг: сервер уже запущен
 
    subprocess.run(
        [
            sys.executable,
            "-m", "streamlit",
            "run",
            __file__,
            "--server.headless", "false",
        ],
        env=env,
        check=True,
    )
    sys.exit(0)   # завершаем родительский процесс после старта сервера