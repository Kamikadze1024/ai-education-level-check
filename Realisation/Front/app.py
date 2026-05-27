"""
AI EdTech Exam — Flask Application Factory
"""

from flask import Flask
from routes import register_routes


def create_app() -> Flask:
    """Создаёт и конфигурирует Flask-приложение."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.secret_key = "edtech-exam-secret-2024"

    register_routes(app)
    return app
