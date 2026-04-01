"""
views/main_view.py — Главная страница (заглушка).

Отображается после успешной аутентификации.
Здесь будет основной функционал нейроэкзаменатора.
"""

import streamlit as st


def render():
    """Рендер главной страницы. Вызывается из main.py."""

    # ── Шапка: название + кнопка выхода ────────────────────────
    col_title, col_btn = st.columns([5, 1])

    with col_title:
        st.markdown(
            f"""
            <div style="font-size:22px; font-weight:600; letter-spacing:0.1em;
                        color:#d6e8f7; padding-top:8px;">
                🧠&nbsp;AI EdTech Exam
                <span style="font-family:'Fira Code',monospace; font-size:12px;
                             color:#1a8fe3; margin-left:12px;">
                    // {st.session_state.username}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_btn:
        # Кнопка выхода — сбрасывает сессию и возвращает на страницу входа
        if st.button("Выйти", key="btn_logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

    st.markdown(
        "<hr style='border:none; border-top:1px solid #1e2d42; margin:12px 0 40px;'/>",
        unsafe_allow_html=True,
    )

    # ── Заглушка контента ───────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding:80px 0;">
            <div style="font-size:48px; opacity:0.25; margin-bottom:16px;">⚙️</div>
            <div style="font-family:'Fira Code',monospace; font-size:13px;
                        color:#1e2d42; letter-spacing:0.2em; text-transform:uppercase;">
                // главная страница — в разработке
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
