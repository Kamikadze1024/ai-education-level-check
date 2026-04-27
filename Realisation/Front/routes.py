"""
AI EdTech Exam — Routes
Проксирует запросы к бэкенду (localhost:8000) и отдаёт HTML-страницы.
"""

import requests
from flask import (
    Flask, render_template, request,
    jsonify, Response
)

BACKEND_URL = "http://localhost:8000"
TIMEOUT = 15  # секунд


def _proxy_post(path: str, **kwargs) -> Response:
    """Универсальный POST-прокси к бэкенду."""
    try:
        resp = requests.post(f"{BACKEND_URL}{path}", timeout=TIMEOUT, **kwargs)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "backend_unavailable"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _proxy_get(path: str, **kwargs) -> Response:
    """Универсальный GET-прокси к бэкенду."""
    try:
        resp = requests.get(f"{BACKEND_URL}{path}", timeout=TIMEOUT, **kwargs)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "backend_unavailable"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def register_routes(app: Flask):
    """Регистрирует все маршруты приложения."""

    # ─── SPA Shell ────────────────────────────────────────────────────────────

    @app.route("/")
    def index():
        return render_template("index.html")

    # ─── Auth proxy ───────────────────────────────────────────────────────────

    @app.route("/api/auth", methods=["POST"])
    def auth():
        data = request.get_json()
        return _proxy_post("/core/auth", json=data)

    # ─── Admin: Knowledge Base ─────────────────────────────────────────────────

    @app.route("/api/upload_know_base", methods=["POST"])
    def upload_know_base():
        try:
            files = request.files
            file_obj = files.get("file")
            if not file_obj:
                return jsonify({"error": "no_file"}), 400

            resp = requests.post(
                f"{BACKEND_URL}/gen/upload_know_base",
                files={"file": (file_obj.filename, file_obj.stream, file_obj.content_type)},
                timeout=60,
            )
            if resp.status_code == 200:
                return jsonify({"result": "ok"}), 200
            else:
                # Пытаемся вернуть тело ответа как есть
                try:
                    body = resp.json()
                except Exception:
                    body = {"error": resp.text or "upload_failed"}
                return jsonify(body), resp.status_code
        except requests.exceptions.ConnectionError:
            return jsonify({"error": "backend_unavailable"}), 503
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ─── Admin: Generate Questions ─────────────────────────────────────────────

    @app.route("/api/generate_questions", methods=["POST"])
    def generate_questions():
        data = request.get_json()
        return _proxy_post("/gen/questions", json=data)

    # ─── Admin: Save Questions ─────────────────────────────────────────────────

    @app.route("/api/save_questions", methods=["POST"])
    def save_questions():
        data = request.get_json()
        return _proxy_post("/gen/save_questions", json=data)

    # ─── Student: Get Available Exams ──────────────────────────────────────────

    @app.route("/api/get_available_exams", methods=["GET"])
    def get_available_exams():
        return _proxy_get("/exam/get_available_exams")
    

    # ─── Student: Get Exam By ID ───────────────────────────────────────────────

    @app.route("/api/get_exam_by_id", methods=["POST"])
    def get_exam_by_id():
        data = request.get_json()
        return _proxy_post("/exam/get_exam_by_id", json=data)

    # ─── Student: Execute Exam ─────────────────────────────────────────────────

    @app.route("/api/execute_exam", methods=["POST"])
    def execute_exam():
        data = request.get_json()
        return _proxy_post("/exam/execute", json=data)
