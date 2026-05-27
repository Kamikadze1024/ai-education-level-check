"""
AI EdTech Exam — Main Entry Point
Запускает веб-сервер (Flask) и открывает окно pywebview.
"""

import sys
import threading
import webview
from app import create_app

def start_server(app):
    """Запуск Flask в отдельном потоке."""
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)

def main():
    app = create_app()

    # Запускаем Flask-сервер в фоне
    server_thread = threading.Thread(target=start_server, args=(app,), daemon=True)
    server_thread.start()

    # Небольшая пауза, чтобы сервер успел подняться
    import time
    time.sleep(0.8)

    # Открываем окно pywebview
    window = webview.create_window(
        title="AI EdTech Exam",
        url="http://127.0.0.1:5050/",
        width=1440,
        height=900,
        min_size=(1024, 700),
        resizable=True,
        text_select=False,
    )

    webview.start(debug=False)

if __name__ == "__main__":
    main()
