"""
theme/global_styles.py — Тёмная CSS-тема приложения.

Вызывается один раз из main.py через inject_styles().
"""

import streamlit as st


def inject_styles():
    """Внедряет CSS тёмной темы через st.markdown."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500&display=swap');

        /* ── Цветовая палитра ── */
        :root {
            --bg-deep:     #080c14;
            --bg-card:     #0e1520;
            --bg-input:    #121b28;
            --border:      #1e2d42;
            --border-glow: #1a6faa;
            --accent:      #1a8fe3;
            --accent-dim:  #0f5a94;
            --accent-glow: rgba(26,143,227,0.25);
            --text:        #d6e8f7;
            --text-muted:  #4a6880;
            --text-error:  #e05252;
        }

        /* ── Фон приложения ── */
        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"] {
            background-color: var(--bg-deep) !important;
        }
        [data-testid="stApp"] {
            background: radial-gradient(ellipse at 50% 0%, #0d1825 0%, var(--bg-deep) 70%) !important;
        }

        /* ── Скрываем меню и футер Streamlit ── */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Шрифт ── */
        * { font-family: 'Rajdhani', sans-serif; color: var(--text); }

        /* ── Поля ввода ── */
        [data-testid="stTextInput"] input {
            background-color: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: 6px !important;
            color: var(--text) !important;
            font-family: 'Fira Code', monospace !important;
            font-size: 15px !important;
            caret-color: var(--accent);
            transition: border-color 0.25s, box-shadow 0.25s;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: var(--border-glow) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }
        [data-testid="stTextInput"] label,
        [data-testid="stTextInput"] p {
            color: var(--text-muted) !important;
            font-size: 12px !important;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        /* ── Кнопка ── */
        [data-testid="stButton"] button {
            background: linear-gradient(135deg, var(--accent-dim), var(--accent)) !important;
            border: none !important;
            border-radius: 6px !important;
            color: #fff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            width: 100% !important;
            transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
        }
        [data-testid="stButton"] button:hover {
            opacity: 0.88 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 24px var(--accent-glow) !important;
        }
        [data-testid="stButton"] button:active {
            transform: translateY(0) !important;
        }

        /* ── Блок ошибки ── */
        [data-testid="stAlert"] {
            background-color: rgba(224,82,82,0.08) !important;
            border: 1px solid rgba(224,82,82,0.35) !important;
            border-radius: 6px !important;
        }

        /* ── Анимация появления ── */
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(16px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .fade-up { animation: fadeUp 0.5s cubic-bezier(0.22,1,0.36,1) both; }

        /* ── Сканирующая линия ── */
        @keyframes scan {
            from { top: -4px; }
            to   { top: 100%; }
        }
        .scanline {
            position: fixed; left: 0; width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-glow), transparent);
            animation: scan 6s linear infinite;
            pointer-events: none; z-index: 9999;
        }

        /* ── Скроллбар ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-deep); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
        </style>

        <div class="scanline"></div>
        """,
        unsafe_allow_html=True,
    )
