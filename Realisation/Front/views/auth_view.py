"""
views/auth_view.py — Страница аутентификации.

Отображает форму входа (логин + пароль + кнопка «Войти»).
При нажатии кнопки вызывает backend_client.authenticate(),
обрабатывает ответ и либо переводит на страницу экзамена,
либо показывает сообщение об ошибке.
"""

import streamlit as st
from backend.backend_client import authenticate


def render():
    """Вызывается из main.py когда authenticated == False."""

    # Отступ сверху для визуального центрирования карточки
    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

    # Три колонки — контент только в центральной (пропорция 1 : 1.6 : 1)
    col_left, col_center, col_right = st.columns([1, 1.6, 1])

    with col_center:

        # ── Шапка: иконка + название + подзаголовок ────────────
        # ИСПРАВЛЕНО: название «AI EDTECH EXAM» как на макете
        st.markdown(
            """
            <div class="auth-card" style="text-align:center; margin-bottom:32px;">

                <div style="
                    font-size:56px; line-height:1; margin-bottom:14px;
                    filter:drop-shadow(0 0 14px rgba(200,120,255,0.55));
                ">🧠</div>

                <div style="
                    font-family:'Rajdhani',sans-serif;
                    font-size:30px; font-weight:700;
                    letter-spacing:0.18em; text-transform:uppercase;
                    color:#d6e8f7;
                ">AI EDTECH EXAM</div>

                <div style="
                    font-family:'Fira Code',monospace;
                    font-size:12px; letter-spacing:0.28em;
                    color:#1a8fe3; margin-top:6px;
                    text-transform:uppercase;
                ">// система оценки знаний</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Разделитель ─────────────────────────────────────────
        st.markdown(
            "<hr style='border-top:1px solid #1e2d42; margin-bottom:28px;'/>",
            unsafe_allow_html=True,
        )

        # ── Поля ввода ──────────────────────────────────────────
        login = st.text_input(
            label="Логин",
            placeholder="введите логин",
            key="auth_login",
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        password = st.text_input(
            label="Пароль",
            placeholder="введите пароль",
            type="password",
            key="auth_password",
        )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Место для ошибки — резервируем заранее чтобы страница не прыгала
        error_placeholder = st.empty()

        # ── Кнопка «Войти» ──────────────────────────────────────
        if st.button("Войти", key="auth_submit", use_container_width=True):
            _handle_login(login, password, error_placeholder)

        # ── Нижняя подпись ──────────────────────────────────────
        st.markdown(
            """
            <div style="
                text-align:center; margin-top:32px;
                font-family:'Fira Code',monospace;
                font-size:11px; color:#1e2d42; letter-spacing:0.2em;
            ">v1.0.0 · SECURE CONNECTION</div>
            """,
            unsafe_allow_html=True,
        )


def _handle_login(login: str, password: str, error_placeholder):
    """
    Обрабатывает нажатие «Войти»:
    1. Проверяет что поля не пустые.
    2. Вызывает authenticate() из backend_client.
    3. Успех → session_state + st.rerun().
    4. Ошибка → выводит сообщение в error_placeholder.
    """
    if not login.strip():
        error_placeholder.error("⚠ Введите логин.")
        return

    if not password.strip():
        error_placeholder.error("⚠ Введите пароль.")
        return

    with st.spinner("Проверка данных..."):
        result = authenticate(login=login.strip(), password=password)

    if result["success"]:
        st.session_state.authenticated = True
        st.session_state.username = login.strip()
        st.rerun()
    else:
        error_placeholder.error(f"✗ {result['message']}")
