"""
main.py — Точка входа фронтенда нейроэкзаменатора.

Запуск:
    python main.py
"""

import sys
import os
import streamlit as st
from views.auth_view import render as render_auth
from views.exam_view import render as render_exam   # ← НОВОЕ: страница экзамена
from theme.global_styles import inject_styles



sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))



st.set_page_config(
    page_title="НейроЭкзаменатор",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)



# Инициализация состояния сеанса при первом запуске
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

inject_styles()

# Маршрутизация:
#   не авторизован → страница входа
#   авторизован    → страница экзамена  ← ИЗМЕНЕНО: было render_main()
if st.session_state.authenticated:
    render_exam()
else:
    render_auth()



if __name__ == "__main__" and os.environ.get("STREAMLIT_RUNNING") != "1":
    import subprocess

    env = os.environ.copy()
    env["STREAMLIT_RUNNING"] = "1"

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
    sys.exit(0)