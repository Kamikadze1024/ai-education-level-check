"""
pages/main_page.py — Главная страница (заглушка).

Отображается после успешной аутентификации.
Здесь в будущем будет основной функционал нейроэкзаменатора.
"""

import streamlit as st


def render():
    """
    Рендер главной страницы.
    Вызывается из main.py, когда st.session_state.authenticated == True.
    """

    # ── Верхняя панель: приветствие + кнопка выхода ────────────
    col_title, col_logout = st.columns([5, 1])

    with col_title:
        st.markdown(
            f"""
            <div style="
                font-family: 'Rajdhani', sans-serif;
                font-size: 22px;
                font-weight: 600;
                letter-spacing: 0.1em;
                color: #d6e8f7;
                padding-top: 8px;
            ">
                🧠&nbsp; НейроЭкзаменатор
                <span style="
                    font-family: 'Fira Code', monospace;
                    font-size: 12px;
                    color: #1a8fe3;
                    margin-left: 12px;
                ">// {st.session_state.username}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_logout:
        # Кнопка выхода — сбрасывает сессию и возвращает на страницу входа
        if st.button("Выйти", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

    # ── Разделитель ─────────────────────────────────────────────
    st.markdown(
        "<hr style='border-top: 1px solid #1e2d42; margin: 12px 0 40px;'/>",
        unsafe_allow_html=True,
    )

    # ── Заглушка основного контента ─────────────────────────────
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 80px 0;
        ">
            <div style="
                font-size: 48px;
                margin-bottom: 16px;
                opacity: 0.3;
            ">⚙️</div>
            <div style="
                font-family: 'Fira Code', monospace;
                font-size: 14px;
                color: #1e2d42;
                letter-spacing: 0.2em;
                text-transform: uppercase;
            ">// главная страница в разработке</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
