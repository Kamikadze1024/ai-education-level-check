"""
styles/global_styles.py — Глобальные CSS-стили тёмной темы.

Вызывается один раз из main.py через inject_styles().
"""

import streamlit as st


def inject_styles():
    """Внедряет CSS-стили тёмной темы через st.markdown."""
    st.markdown(
        """
        <style>
        /* ════════════════════════════════════════════
           ИМПОРТ ШРИФТОВ
           Rajdhani — заголовки (технический, лаконичный)
           Fira Code — моноширинный акцент
        ════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500&display=swap');

        /* ════════════════════════════════════════════
           CSS-ПЕРЕМЕННЫЕ ПАЛИТРЫ
        ════════════════════════════════════════════ */
        :root {
            --bg-deep:      #080c14;
            --bg-card:      #0e1520;
            --bg-input:     #121b28;
            --border:       #1e2d42;
            --border-glow:  #1a6faa;
            --accent:       #1a8fe3;
            --accent-dim:   #0f5a94;
            --accent-glow:  rgba(26,143,227,0.25);
            --text-primary: #d6e8f7;
            --text-muted:   #4a6880;
            --text-error:   #e05252;
            --success:      #2aad7a;
        }

        /* ════════════════════════════════════════════
           СБРОС И БАЗОВЫЙ ФОН
        ════════════════════════════════════════════ */
        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"] {
            background-color: var(--bg-deep) !important;
        }

        [data-testid="stApp"] {
            background: radial-gradient(ellipse at 50% 0%,
                #0d1825 0%, var(--bg-deep) 70%) !important;
        }

        /* Скрываем меню, футер и header Streamlit */
        #MainMenu, footer, header { visibility: hidden; }

        /* ════════════════════════════════════════════
           ГЛОБАЛЬНАЯ ТИПОГРАФИКА
           ИЗМЕНЕНО: базовый размер шрифта увеличен с 14px до 16px
        ════════════════════════════════════════════ */
        * {
            font-family: 'Rajdhani', sans-serif;
            color: var(--text-primary);
        }

        /* Общий размер текста для всего приложения */
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"] {
            font-size: 16px !important;
        }

        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        /* ════════════════════════════════════════════
           ТЕКСТОВЫЕ ПОЛЯ ВВОДА (auth: логин, пароль)
           ИЗМЕНЕНО: font-size шрифта текста и лейбла увеличен
        ════════════════════════════════════════════ */
        [data-testid="stTextInput"] input,
        [data-testid="stTextInput"] input:focus {
            background-color: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: 6px !important;
            color: var(--text-primary) !important;
            font-family: 'Fira Code', monospace !important;
            font-size: 16px !important;          /* ИЗМЕНЕНО: было 15px */
            padding: 10px 14px !important;
            transition: border-color 0.25s ease, box-shadow 0.25s ease;
            caret-color: var(--accent);
        }

        [data-testid="stTextInput"] input:focus {
            border-color: var(--border-glow) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
            outline: none !important;
        }

        /* Лейблы полей ЛОГИН / ПАРОЛЬ */
        [data-testid="stTextInput"] label,
        [data-testid="stTextInput"] label p,
        [data-testid="stTextInput"] > div > label {
            color: var(--text-muted) !important;
            font-size: 15px !important;          /* ИЗМЕНЕНО: было 13px */
            font-weight: 600 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            font-family: 'Rajdhani', sans-serif !important;
            visibility: visible !important;
            display: block !important;
        }

        /* ════════════════════════════════════════════
           КНОПКИ (все кнопки приложения)
           ИЗМЕНЕНО: font-size увеличен
        ════════════════════════════════════════════ */
        [data-testid="stButton"] button {
            background: linear-gradient(135deg,
                var(--accent-dim) 0%, var(--accent) 100%) !important;
            border: none !important;
            border-radius: 6px !important;
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 18px !important;          /* ИЗМЕНЕНО: было 16px */
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            padding: 12px 0 !important;
            text-transform: uppercase !important;
            width: 100% !important;
            transition: opacity 0.2s ease, transform 0.15s ease,
                        box-shadow 0.2s ease;
            cursor: pointer;
        }

        [data-testid="stButton"] button:hover {
            opacity: 0.88 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 24px var(--accent-glow) !important;
        }

        [data-testid="stButton"] button:active {
            transform: translateY(0) !important;
            opacity: 0.95 !important;
        }

        /* ════════════════════════════════════════════
           БЛОК ОШИБКИ / ПРЕДУПРЕЖДЕНИЯ
        ════════════════════════════════════════════ */
        [data-testid="stAlert"] {
            background-color: rgba(224, 82, 82, 0.08) !important;
            border: 1px solid rgba(224, 82, 82, 0.35) !important;
            border-radius: 6px !important;
            color: var(--text-error) !important;
            font-size: 15px !important;          /* ИЗМЕНЕНО: добавлен размер */
        }

        /* ════════════════════════════════════════════
           АНИМАЦИЯ ПОЯВЛЕНИЯ КАРТОЧКИ ВХОДА
        ════════════════════════════════════════════ */
        @keyframes fadeSlideIn {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .auth-card {
            animation: fadeSlideIn 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
        }

        /* Сканирующая линия — декоративный эффект */
        @keyframes scanline {
            0%   { top: -4px; }
            100% { top: 100%; }
        }

        .scanline {
            position: fixed;
            left: 0; width: 100%;
            height: 2px;
            background: linear-gradient(90deg,
                transparent 0%, var(--accent-glow) 50%, transparent 100%);
            animation: scanline 6s linear infinite;
            pointer-events: none;
            z-index: 9999;
        }

        /* ════════════════════════════════════════════
           ГОРИЗОНТАЛЬНЫЙ РАЗДЕЛИТЕЛЬ
        ════════════════════════════════════════════ */
        hr {
            border: none !important;
            border-top: 1px solid var(--border) !important;
            margin: 20px 0 !important;
        }

        /* ════════════════════════════════════════════
           ВИДЖЕТ ЗАГРУЗКИ ФАЙЛОВ
           ИЗМЕНЕНО: font-size надписей увеличен
        ════════════════════════════════════════════ */
        [data-testid="stFileUploader"] {
            background: var(--bg-input) !important;
            border: 1px dashed var(--border-glow) !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: var(--accent) !important;
        }
        [data-testid="stFileUploaderDropzone"] {
            background: transparent !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] p,
        [data-testid="stFileUploaderDropzoneInstructions"] span {
            color: var(--text-muted) !important;
            font-family: 'Fira Code', monospace !important;
            font-size: 15px !important;          /* ИЗМЕНЕНО: было 13px */
        }

        /* ════════════════════════════════════════════
           ЧИСЛОВЫЕ ПОЛЯ ВВОДА (number_input)
           ИЗМЕНЕНО: font-size увеличен
        ════════════════════════════════════════════ */
        [data-testid="stNumberInput"] input {
            background-color: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: 6px !important;
            color: var(--text-primary) !important;
            font-family: 'Fira Code', monospace !important;
            font-size: 16px !important;          /* ИЗМЕНЕНО: было 15px */
        }
        [data-testid="stNumberInput"] input:focus {
            border-color: var(--border-glow) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }
        [data-testid="stNumberInput"] label,
        [data-testid="stNumberInput"] label p {
            color: var(--text-muted) !important;
            font-size: 15px !important;          /* ИЗМЕНЕНО: было 12px */
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        /* Кнопки +/- у числового поля */
        [data-testid="stNumberInput"] button {
            background: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
            width: auto !important;
            font-size: 16px !important;
        }
        [data-testid="stNumberInput"] button:hover {
            border-color: var(--accent) !important;
            transform: none !important;
            box-shadow: none !important;
        }

        /* ════════════════════════════════════════════
           ПРОГРЕСС-БАР
        ════════════════════════════════════════════ */
        [data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg,
                var(--accent-dim), var(--accent)) !important;
            border-radius: 4px !important;
        }
        [data-testid="stProgress"] > div {
            background: var(--bg-input) !important;
            border-radius: 4px !important;
        }

        /* ════════════════════════════════════════════
           СКРОЛЛБАР
        ════════════════════════════════════════════ */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-deep); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--border-glow); }
        </style>

        <!-- Анимированная сканирующая линия поверх страницы -->
        <div class="scanline"></div>
        """,
        unsafe_allow_html=True,
    )
