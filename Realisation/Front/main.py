"""
main.py — Точка входа фронтенда нейроэкзаменатора.

pip install -r requirements.txt


Запуск:
    streamlit run main.py

Логика маршрутизации:
    authenticated == False  →  страница входа  (views/auth_view.py)
    authenticated == True   →  главная страница (views/main_view.py)

Состояние сессии (st.session_state):
    authenticated (bool) — флаг успешного входа
    username      (str)  — логин вошедшего пользователя

ВАЖНО: папка называется views/, а НЕ pages/ —
папка pages/ зарезервирована Streamlit и вызывает конфликт импортов.
"""

import sys
import os

# Добавляем папку проекта в sys.path — чтобы Python находил
# пакеты views/, theme/, backend/ при любом способе запуска.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# set_page_config обязан быть первым вызовом Streamlit
st.set_page_config(
    page_title="НейроЭкзаменатор",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from views.auth_view import render as render_auth    # страница входа
from views.main_view import render as render_main    # главная страница
from theme.global_styles import inject_styles        # тёмная CSS-тема

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
