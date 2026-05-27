"""
AI EdTech Exam — Backend Compatibility Checker
Запусти этот скрипт пока бэкенд работает:
    python check_backend.py

Скрипт проверит каждый эндпоинт и покажет точно что работает, что нет и почему.
"""

import json
import sys
import os
import requests

BACKEND = "http://localhost:8000"
TIMEOUT = 8

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

results = []

def ok(label, detail=""):
    msg = f"  {GREEN}✓ PASS{RESET}  {label}"
    if detail:
        msg += f"\n         {CYAN}{detail}{RESET}"
    print(msg)
    results.append(("PASS", label))

def fail(label, detail=""):
    msg = f"  {RED}✗ FAIL{RESET}  {label}"
    if detail:
        msg += f"\n         {RED}{detail}{RESET}"
    print(msg)
    results.append(("FAIL", label))

def warn(label, detail=""):
    msg = f"  {YELLOW}⚠ WARN{RESET}  {label}"
    if detail:
        msg += f"\n         {YELLOW}{detail}{RESET}"
    print(msg)
    results.append(("WARN", label))

def section(title):
    print(f"\n{BOLD}{CYAN}{'─'*55}{RESET}")
    print(f"{BOLD} {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*55}{RESET}")

def show_response(resp):
    """Печатает статус и тело ответа для диагностики."""
    print(f"         HTTP {resp.status_code}  |  body: {resp.text[:300]}")

# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{BOLD}AI EdTech Exam — Backend Compatibility Check{RESET}")
print(f"Target: {CYAN}{BACKEND}{RESET}\n")

# ══════════════════════════════════════════
# 0. Доступность бэкенда
# ══════════════════════════════════════════
section("0 · Доступность бэкенда")
try:
    r = requests.get(BACKEND, timeout=TIMEOUT)
    ok("Бэкенд отвечает на GET /", f"HTTP {r.status_code}")
except requests.exceptions.ConnectionError:
    fail("Бэкенд НЕДОСТУПЕН на localhost:8000",
         "Убедись что бэкенд запущен перед запуском этого скрипта")
    print(f"\n{RED}Дальнейшие тесты невозможны — бэкенд не отвечает.{RESET}\n")
    sys.exit(1)
except Exception as e:
    warn(f"GET / вернул ошибку: {e}")

# ══════════════════════════════════════════
# 1. POST /core/auth
# ══════════════════════════════════════════
section("1 · POST /core/auth")

admin_login = student_login = None  # заполним если угадаем

for login, password, role_hint in [
    ("admin",   "admin",   "admin"),
    ("admin",   "password","admin"),
    ("student", "student", "student"),
    ("student", "password","student"),
    ("user",    "user",    "student"),
    ("test",    "test",    "any"),
]:
    try:
        r = requests.post(f"{BACKEND}/core/auth",
                          json={"login": login, "password": password},
                          timeout=TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            if data.get("result") == "ok":
                role = data.get("role", "?")
                ok(f'auth login="{login}" pwd="{password}" → result=ok role={role}',
                   f"Ответ: {data}")
                if role == "admin"   and admin_login is None:
                    admin_login = (login, password)
                if role == "student" and student_login is None:
                    student_login = (login, password)
            elif data.get("result") == "fail":
                pass  # молча пропускаем неверные
            else:
                warn(f'auth login="{login}" → неожиданный ответ', str(data))
        else:
            warn(f'auth login="{login}" → HTTP {r.status_code}', r.text[:200])
    except Exception as e:
        fail(f'auth login="{login}" → исключение: {e}')

# Проверяем формат fail
try:
    r = requests.post(f"{BACKEND}/core/auth",
                      json={"login": "wrong__xyz", "password": "wrong__xyz"},
                      timeout=TIMEOUT)
    data = r.json()
    if data.get("result") == "fail":
        ok('auth с неверными данными → {"result":"fail"}')
    elif data.get("result") == "ok":
        warn("auth с неверными данными вернул ok — возможно любой логин проходит?",
             str(data))
    else:
        warn("auth с неверными данными вернул неожиданный формат", str(data))
    show_response(r)
except Exception as e:
    fail(f"auth fail-тест → {e}")

if not admin_login and not student_login:
    warn("Не удалось угадать ни одного логина/пароля",
         "Введи свои данные в переменные ADMIN_LOGIN/STUDENT_LOGIN ниже")

# Ручные данные — если знаешь свои логины, впиши сюда:
ADMIN_LOGIN   = admin_login   or ("admin",   "admin")
STUDENT_LOGIN = student_login or ("student", "student")

print(f"\n  Будем использовать для дальнейших тестов:")
print(f"    admin   → {ADMIN_LOGIN}")
print(f"    student → {STUDENT_LOGIN}")

# ══════════════════════════════════════════
# 2. POST /gen/upload_know_base
# ══════════════════════════════════════════
section("2 · POST /gen/upload_know_base")

# Создаём минимальный тестовый файл
test_file_path = "/tmp/test_knowledge.txt"
with open(test_file_path, "w") as f:
    f.write("Это тестовая база знаний.\nПитон — язык программирования.\nФлask — веб-фреймворк.")

try:
    with open(test_file_path, "rb") as f:
        r = requests.post(
            f"{BACKEND}/gen/upload_know_base",
            files={"file": ("test_knowledge.txt", f, "text/plain")},
            timeout=30,
        )
    print(f"  Загрузка файла:")
    show_response(r)

    if r.status_code == 200:
        ok("/gen/upload_know_base → HTTP 200", r.text[:200])
    else:
        fail(f"/gen/upload_know_base → HTTP {r.status_code}", r.text[:300])

    # Проверяем имя поля — может быть не "file"
    if r.status_code != 200:
        for field_name in ["file", "document", "knowledge_base", "kb", "upload"]:
            with open(test_file_path, "rb") as f2:
                r2 = requests.post(
                    f"{BACKEND}/gen/upload_know_base",
                    files={field_name: ("test_knowledge.txt", f2, "text/plain")},
                    timeout=30,
                )
            if r2.status_code == 200:
                ok(f"Работает с field_name='{field_name}'",
                   "⚠ В routes.py замени request.files.get('file') на request.files.get('{field_name}')")
                break
            else:
                print(f"  field_name='{field_name}' → HTTP {r2.status_code}")

except Exception as e:
    fail(f"/gen/upload_know_base → исключение: {e}")

# ══════════════════════════════════════════
# 3. POST /gen/questions
# ══════════════════════════════════════════
section("3 · POST /gen/questions")

generated_questions = None
try:
    payload = {
        "num_questions": 2,
        "num_answ_per_one_quest": 4,
        "num_correct_answ_per_one_quest": 1,
    }
    r = requests.post(f"{BACKEND}/gen/questions", json=payload, timeout=60)
    print(f"  Запрос: {json.dumps(payload)}")
    show_response(r)

    if r.status_code == 200:
        data = r.json()
        if data.get("msg_type") == "questions_list" and "questions" in data:
            ok(f'/gen/questions → questions_list с {len(data["questions"])} вопросами')
            generated_questions = data["questions"]

            # Проверяем структуру вопросов
            q = data["questions"][0] if data["questions"] else {}
            has_num    = "question_num" in q
            has_txt    = "question_txt" in q
            has_correct = "correct_answs" in q
            has_wrong   = "not_correct_answs" in q

            if has_num and has_txt and has_correct and has_wrong:
                ok("Структура вопроса корректна (question_num, question_txt, correct_answs, not_correct_answs)")
            else:
                missing = [f for f, v in [("question_num",has_num),("question_txt",has_txt),
                           ("correct_answs",has_correct),("not_correct_answs",has_wrong)] if not v]
                warn(f"В вопросе отсутствуют поля: {missing}", f"Пример вопроса: {q}")
        else:
            warn(f'/gen/questions → HTTP 200 но формат неожиданный', str(data)[:300])
    else:
        fail(f'/gen/questions → HTTP {r.status_code}')

except Exception as e:
    fail(f"/gen/questions → исключение: {e}")

# ══════════════════════════════════════════
# 4. POST /gen/save_questions
# ══════════════════════════════════════════
section("4 · POST /gen/save_questions")

saved_exam_id = None
if generated_questions:
    try:
        r = requests.post(f"{BACKEND}/gen/save_questions",
                          json={"questions": generated_questions},
                          timeout=TIMEOUT)
        show_response(r)

        if r.status_code == 200:
            data = r.json()
            if "quest_list_id" in data:
                saved_exam_id = data["quest_list_id"]
                ok(f'/gen/save_questions → quest_list_id={saved_exam_id}')
            else:
                warn("/gen/save_questions → HTTP 200 но нет поля quest_list_id", str(data))
        else:
            fail(f'/gen/save_questions → HTTP {r.status_code}')
    except Exception as e:
        fail(f"/gen/save_questions → исключение: {e}")
else:
    warn("/gen/save_questions — пропущен (нет сгенерированных вопросов)")

# ══════════════════════════════════════════
# 5. GET /exam/get_available_exams
# ══════════════════════════════════════════
section("5 · GET /exam/get_available_exams")

available_exam_id = None
try:
    r = requests.get(f"{BACKEND}/exam/get_available_exams", timeout=TIMEOUT)
    show_response(r)

    if r.status_code == 200:
        data = r.json()
        if "available_exams" in data:
            exams = data["available_exams"]
            ok(f'/exam/get_available_exams → {len(exams)} экзаменов')
            if exams:
                available_exam_id = exams[0].get("available_exam_id")
                ok(f'Первый available_exam_id={available_exam_id}')
                # Проверяем структуру
                if "available_exam_id" not in exams[0]:
                    warn("Поле называется не 'available_exam_id'", str(exams[0]))
        else:
            warn("/exam/get_available_exams → нет поля 'available_exams'", str(data))
    else:
        fail(f'/exam/get_available_exams → HTTP {r.status_code}')
except Exception as e:
    fail(f"/exam/get_available_exams → исключение: {e}")

# ══════════════════════════════════════════
# 6. POST /exam/execute
# ══════════════════════════════════════════
section("6 · POST /exam/execute")

try:
    payload = {
        "msg_type": "exam_procedure",
        "exam_id": available_exam_id or 1,
        "answers": [],
    }
    r = requests.post(f"{BACKEND}/exam/execute", json=payload, timeout=TIMEOUT)
    print(f"  Запрос: {json.dumps(payload)}")
    show_response(r)

    if r.status_code == 200:
        data = r.json()
        if "correct_answs" in data and "incorrect_answs" in data:
            ok(f'/exam/execute → correct={data["correct_answs"]} incorrect={data["incorrect_answs"]}')
        else:
            warn("/exam/execute → HTTP 200 но формат ответа неожиданный", str(data))
    else:
        fail(f'/exam/execute → HTTP {r.status_code}')
except Exception as e:
    fail(f"/exam/execute → исключение: {e}")

# ══════════════════════════════════════════
# 7. Проверка CORS (если фронт на другом порту)
# ══════════════════════════════════════════
section("7 · CORS headers")

try:
    r = requests.options(f"{BACKEND}/core/auth", timeout=TIMEOUT,
                         headers={"Origin": "http://127.0.0.1:5050",
                                  "Access-Control-Request-Method": "POST"})
    cors = r.headers.get("Access-Control-Allow-Origin", "")
    if cors:
        ok(f"CORS разрешён: Access-Control-Allow-Origin: {cors}")
    else:
        warn("CORS заголовки отсутствуют",
             "Это НЕ проблема если фронт работает через Flask-прокси (наш случай)")
except Exception as e:
    warn(f"OPTIONS /core/auth → {e}")

# ══════════════════════════════════════════
# ИТОГ
# ══════════════════════════════════════════
section("ИТОГ")

passes = sum(1 for s, _ in results if s == "PASS")
fails  = sum(1 for s, _ in results if s == "FAIL")
warns  = sum(1 for s, _ in results if s == "WARN")

print(f"\n  {GREEN}PASS: {passes}{RESET}   {RED}FAIL: {fails}{RESET}   {YELLOW}WARN: {warns}{RESET}\n")

if fails == 0 and warns == 0:
    print(f"  {GREEN}{BOLD}✓ Бэкенд полностью совместим с фронтом!{RESET}")
elif fails == 0:
    print(f"  {YELLOW}{BOLD}⚠ Есть предупреждения — фронт может работать с ограничениями.{RESET}")
else:
    print(f"  {RED}{BOLD}✗ Есть проблемы совместимости — см. FAIL выше.{RESET}")

print(f"""
  Что делать дальше:
  1. Скопируй весь вывод этого скрипта
  2. Вставь сюда в чат
  3. Я точно скажу что нужно поправить во фронте (routes.py / app.js)
""")
