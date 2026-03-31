"""
views/auth_view.py — Страница аутентификации.

Показывает форму: логин + пароль + кнопка «Войти».
При нажатии вызывает backend_client.authenticate(),
и либо переходит на главную, либо показывает ошибку.
"""

import streamlit as st
from backend.backend_client import authenticate


def render():
    """Рендер страницы входа. Вызывается из main.py."""

    # Отступ сверху для визуального центрирования
    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

    # Центрирование карточки колонками
    _, col, _ = st.columns([1, 1.6, 1])

    with col:

        # ── Шапка ───────────────────────────────────────────────
        st.markdown(
            """
            <div class="fade-up" style="text-align:center; margin-bottom:32px;">
                <div style="font-size:52px; line-height:1; margin-bottom:12px;
                            filter:drop-shadow(0 0 14px rgba(26,143,227,0.65));">
                    🧠
                </div>
                <div style="font-size:28px; font-weight:700; letter-spacing:0.15em;
                            text-transform:uppercase; color:#d6e8f7;">
                    AI EdTech Exam
                </div>
                <div style="font-family:'Fira Code',monospace; font-size:11px;
                            letter-spacing:0.25em; color:#1a8fe3; margin-top:4px;">
                    // система оценки знаний
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<hr style='border:none; border-top:1px solid #1e2d42; margin-bottom:24px;'/>",
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

        # Место для вывода ошибки (появляется между полями и кнопкой)
        error_slot = st.empty()

        # ── Кнопка «Войти» ──────────────────────────────────────
        if st.button("Войти", key="btn_login", use_container_width=True):
            _handle_login(login, password, error_slot)

        # ── Версия ──────────────────────────────────────────────
        st.markdown(
            "<div style='text-align:center; margin-top:32px; font-family:Fira Code,monospace;"
            "font-size:10px; color:#1e2d42; letter-spacing:0.2em;'>v1.0.0 · SECURE</div>",
            unsafe_allow_html=True,
        )


def _handle_login(login: str, password: str, error_slot):
    """
    Обрабатывает нажатие кнопки «Войти»:
    1. Проверяет, что поля не пустые.
    2. Вызывает authenticate() из backend_client.
    3. Успех → выставляет флаг и перезагружает страницу.
    4. Ошибка → показывает сообщение.
    """
    # Валидация на стороне фронта
    if not login.strip():
        error_slot.error("⚠ Введите логин.")
        return
    if not password.strip():
        error_slot.error("⚠ Введите пароль.")
        return

    # Запрос к бэкенду
    with st.spinner("Проверка..."):
        result = authenticate(login=login.strip(), password=password)

    if result["success"]:
        # Сохраняем сессию и переходим на главную
        st.session_state.authenticated = True
        st.session_state.username = login.strip()
        st.rerun()
    else:
        error_slot.error(f"✗ {result['message']}")
