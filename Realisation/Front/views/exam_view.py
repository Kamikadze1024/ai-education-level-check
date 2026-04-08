"""
views/exam_view.py — Страница подготовки экзамена.

══════════════════════════════════════════════════════
🔌 РУЧКА ДЛЯ ИНТЕГРАЦИИ С БЭКЕНДОМ:

    Метод : POST
    URL   : {BACKEND_URL}/generate
    Тело  : multipart/form-data
                files[]       — файлы (PDF / TXT / DOC / DOCX)
                num_questions — количество вопросов (int)
                num_answers   — количество правильных ответов (int)
    200 OK: {"status": "OK", "questions": [...]}
    Ошибка: любой другой HTTP-статус

    Функция: backend/backend_client.py → generate_questions()

ДЕМО-РЕЖИМ: DEMO_MODE = True в backend_client.py
    → вместо запроса к серверу ждёт 3 сек и возвращает заглушку.
══════════════════════════════════════════════════════
"""

import time
import streamlit as st
from backend.backend_client import generate_questions


def render():
    """Рендер страницы. Вызывается из main.py когда authenticated == True."""

    _render_header()

    st.markdown(
        "<hr style='border-top:1px solid #1e2d42; margin:12px 0 32px;'/>",
        unsafe_allow_html=True,
    )

    uploaded_files = _render_upload_block()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    num_questions, num_answers = _render_params_block()

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    _render_generate_block(uploaded_files, num_questions, num_answers)


# ══════════════════════════════════════════════════════════════
# ПРИВАТНЫЕ ФУНКЦИИ
# ══════════════════════════════════════════════════════════════

def _render_header():
    """Шапка: название + логин + кнопка выхода."""
    col_title, col_logout = st.columns([5, 1])

    with col_title:
        st.markdown(
            f"""
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:22px; font-weight:600;
                letter-spacing:0.1em; color:#d6e8f7; padding-top:8px;
            ">
                🧠&nbsp;AI EdTech Exam
                <span style="
                    font-family:'Fira Code',monospace;
                    font-size:13px; color:#1a8fe3; margin-left:12px;
                ">// {st.session_state.username}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_logout:
        if st.button("Выйти", key="exam_logout_btn"):
            for key in ["authenticated", "username", "generation_result"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


def _render_upload_block():
    """
    Блок загрузки файлов базы знаний.
    Поддерживаемые форматы: PDF, TXT, DOC, DOCX.
    Удалить неверно выбранный файл — нажать крестик × рядом с его именем.
    Возвращает список загруженных файлов (может быть пустым).
    """
    st.markdown(
        """
        <div style="
            font-family:'Rajdhani',sans-serif;
            font-size:20px; font-weight:600;
            letter-spacing:0.06em; color:#d6e8f7; margin-bottom:12px;
        ">
            Загрузите файлы с базой знаний
            <span style="
                font-family:'Fira Code',monospace;
                font-size:15px; color:#4a6880; margin-left:8px;
            ">для подготовки тестов и экзаменационных вопросов</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # type — допустимые форматы; удаление файла — кнопка × у каждого файла
    uploaded_files = st.file_uploader(
        label="Перетащите файлы или нажмите «Browse files»",
        type=["pdf", "txt", "doc", "docx"],
        accept_multiple_files=True,
        key="knowledge_files",
        label_visibility="collapsed",
    )

    if uploaded_files:
        names = ", ".join(f.name for f in uploaded_files)
        st.markdown(
            f"""
            <div style="
                margin-top:12px; font-family:'Fira Code',monospace;
                font-size:15px; color:#2aad7a; letter-spacing:0.05em;
            ">✓ Файлы загружены: {names}</div>
            """,
            unsafe_allow_html=True,
        )

    return uploaded_files


def _render_params_block():
    """
    Панель параметров генерации.
    ИСПРАВЛЕНО: лейблы нарисованы вручную через st.markdown —
    одинаковый шрифт, одинаковый уровень, отступы как у блока загрузки.
    Возвращает кортеж (num_questions, num_answers).
    """
    st.markdown(
        """
        <div style="
            font-family:'Rajdhani',sans-serif;
            font-size:18px; font-weight:600; color:#4a6880;
            letter-spacing:0.08em; text-transform:uppercase; margin-bottom:16px;
        ">Параметры генерации</div>
        """,
        unsafe_allow_html=True,
    )

    col_q, col_a = st.columns(2)

    with col_q:
        # Лейбл рисуем сами — чтобы размер и позиция совпадали с правой колонкой
        st.markdown(
            """
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:15px; font-weight:600; color:#4a6880;
                letter-spacing:0.08em; text-transform:uppercase;
                margin-bottom:6px;
            ">Количество вопросов</div>
            """,
            unsafe_allow_html=True,
        )
        num_questions = st.number_input(
            label="Количество вопросов",   # лейбл скрыт — показан выше
            label_visibility="collapsed",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            key="num_questions",
        )

    with col_a:
        # Лейбл правой колонки — тот же стиль, тот же уровень
        st.markdown(
            """
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:15px; font-weight:600; color:#4a6880;
                letter-spacing:0.08em; text-transform:uppercase;
                margin-bottom:6px;
            ">Количество правильных ответов на вопрос</div>
            """,
            unsafe_allow_html=True,
        )
        num_answers = st.number_input(
            label="Количество правильных ответов",
            label_visibility="collapsed",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key="num_answers",
        )

    return int(num_questions), int(num_answers)


def _render_generate_block(uploaded_files, num_questions: int, num_answers: int):
    """
    Блок запуска генерации.
    ИСПРАВЛЕНО: прогресс-бар работает синхронно в главном потоке —
    убран threading.Thread, который вызывал NoSessionContext в Streamlit.
    """

    # Место для результата — резервируем заранее
    result_slot = st.empty()

    # Показываем сохранённый результат если он есть
    if "generation_result" in st.session_state:
        _show_result(result_slot, st.session_state["generation_result"])

    button_disabled = not bool(uploaded_files)

    if st.button(
        "Составить вопросы",
        key="btn_generate",
        use_container_width=True,
        disabled=button_disabled,
    ):
        if "generation_result" in st.session_state:
            del st.session_state["generation_result"]
        result_slot.empty()

        # ── Прогресс-бар (синхронный, без потоков) ──────────────
        # st.status открывает раскрывающийся блок со статусом.
        # Прогресс обновляется в главном потоке — ошибок нет.
        progress_label = st.empty()
        progress_bar   = st.progress(0)

        progress_label.markdown(
            """
            <div style="
                font-family:'Fira Code',monospace;
                font-size:15px; color:#1a8fe3; margin-bottom:6px;
            ">⟳ Формирую вопросы...</div>
            """,
            unsafe_allow_html=True,
        )

        # Заполняем до 10% немедленно — показываем что процесс начался
        progress_bar.progress(10)

        # ── Запрос к бэкенду (или демо-заглушке) ────────────────
        # Во время выполнения этой функции прогресс стоит на 10%.
        # generate_questions() в демо-режиме сама делает паузу 3 сек.
        result = generate_questions(
            files=uploaded_files,
            num_questions=num_questions,
            num_answers=num_answers,
        )

        # ── Доводим прогресс до 100% плавно после получения ответа
        for i in range(11, 101):
            progress_bar.progress(i)
            time.sleep(0.008)   # ~0.7 сек на финальный прогон

        # Убираем прогресс-бар и метку
        progress_bar.empty()
        progress_label.empty()

        # Сохраняем и показываем результат
        st.session_state["generation_result"] = result
        _show_result(result_slot, result)

    if button_disabled:
        st.markdown(
            """
            <div style="
                margin-top:8px; font-family:'Fira Code',monospace;
                font-size:14px; color:#4a6880;
            ">↑ сначала загрузите файлы</div>
            """,
            unsafe_allow_html=True,
        )


def _show_result(slot, result: dict):
    """Выводит итоговое сообщение: успех (зелёный) или ошибка (красный)."""
    if result["success"]:
        slot.markdown(
            f"""
            <div style="
                margin-top:16px; padding:14px 18px;
                background:rgba(42,173,122,0.10);
                border:1px solid rgba(42,173,122,0.35);
                border-radius:6px; font-family:'Fira Code',monospace;
                font-size:16px; color:#2aad7a; letter-spacing:0.04em;
            ">✓ {result['message']}</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        slot.markdown(
            f"""
            <div style="
                margin-top:16px; padding:14px 18px;
                background:rgba(224,82,82,0.08);
                border:1px solid rgba(224,82,82,0.35);
                border-radius:6px; font-family:'Fira Code',monospace;
                font-size:16px; color:#e05252; letter-spacing:0.04em;
            ">✗ Ошибка: {result['message']}</div>
            """,
            unsafe_allow_html=True,
        )
