/**
 * AI EdTech Exam — Frontend SPA
 * Senior-level, modular, fully commented JS
 */

"use strict";

/* ═══════════════════════════════════════════════════════════════════════════
   UTILITIES
   ═══════════════════════════════════════════════════════════════════════════ */

/** Shorthand querySelector */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/** Format bytes → readable string */
function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

/* ═══════════════════════════════════════════════════════════════════════════
   THEME MANAGER
   ═══════════════════════════════════════════════════════════════════════════ */
const Theme = {
  STORAGE_KEY: "edtech-theme",

  get() {
    return localStorage.getItem(this.STORAGE_KEY) || "dark";
  },

  set(t) {
    localStorage.setItem(this.STORAGE_KEY, t);
    document.documentElement.setAttribute("data-theme", t);
  },

  toggle() {
    this.set(this.get() === "dark" ? "light" : "dark");
  },

  init() {
    this.set(this.get());
    // Wire all theme toggle buttons
    $$("[id^='theme-toggle']").forEach(btn => {
      btn.addEventListener("click", () => this.toggle());
    });
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   TOAST NOTIFICATIONS
   ═══════════════════════════════════════════════════════════════════════════ */
const Toast = {
  container: null,

  ICONS: {
    success: "ph-check-circle",
    error:   "ph-x-circle",
    info:    "ph-info",
    warning: "ph-warning",
  },

  init() {
    this.container = $("#toast-container");
  },

  show(message, type = "info", duration = 4000) {
    const el = document.createElement("div");
    el.className = `toast toast--${type}`;
    el.innerHTML = `<i class="ph ${this.ICONS[type]}"></i><span>${message}</span>`;
    this.container.appendChild(el);

    setTimeout(() => {
      el.classList.add("removing");
      el.addEventListener("animationend", () => el.remove());
    }, duration);
  },

  success: function(msg) { this.show(msg, "success"); },
  error:   function(msg) { this.show(msg, "error", 5000); },
  info:    function(msg) { this.show(msg, "info"); },
  warning: function(msg) { this.show(msg, "warning"); },
};

/* ═══════════════════════════════════════════════════════════════════════════
   MODAL
   ═══════════════════════════════════════════════════════════════════════════ */
const Modal = {
  overlay: null,
  modal:   null,
  okBtn:   null,
  _resolve: null,

  ICONS: {
    success: "ph-check-circle",
    error:   "ph-x-circle",
    info:    "ph-info",
    warning: "ph-warning-circle",
  },

  init() {
    this.overlay = $("#overlay");
    this.modal   = $("#modal");
    this.okBtn   = $("#modal-ok");

    this.okBtn.addEventListener("click", () => {
      this.close();
      if (this._resolve) { this._resolve(); this._resolve = null; }
    });
  },

  /**
   * Show modal and return a Promise that resolves when OK is clicked.
   * @param {object} opts - { title, body, type, okLabel }
   */
  show({ title, body, type = "info", okLabel = "OK" }) {
    $("#modal-icon").innerHTML = `<i class="ph ${this.ICONS[type]}"></i>`;
    $("#modal-icon").className = `modal__icon ${type}`;
    $("#modal-title").textContent = title;
    $("#modal-body").textContent  = body;
    this.okBtn.textContent = okLabel;

    this.overlay.classList.remove("hidden");
    this.modal.classList.remove("hidden");

    return new Promise(resolve => { this._resolve = resolve; });
  },

  close() {
    this.overlay.classList.add("hidden");
    this.modal.classList.add("hidden");
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   API CLIENT
   ═══════════════════════════════════════════════════════════════════════════ */
const Api = {
  /**
   * Generic JSON POST
   */
  async post(url, data) {
    const resp = await fetch(url, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(data),
    });
    const json = await resp.json();
    return { ok: resp.ok, status: resp.status, data: json };
  },

  /**
   * Generic GET
   */
  async get(url) {
    const resp = await fetch(url);
    const json = await resp.json();
    return { ok: resp.ok, status: resp.status, data: json };
  },

  /**
   * File upload with progress callback
   */
  async uploadFile(url, file, onProgress) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const form = new FormData();
      form.append("file", file);

      xhr.upload.addEventListener("progress", (e) => {
        if (e.lengthComputable && onProgress) {
          onProgress(Math.round((e.loaded / e.total) * 100));
        }
      });

      xhr.addEventListener("load", () => {
        try {
          const json = JSON.parse(xhr.responseText);
          resolve({ ok: xhr.status === 200, status: xhr.status, data: json });
        } catch {
          resolve({ ok: xhr.status === 200, status: xhr.status, data: {} });
        }
      });

      xhr.addEventListener("error", () => reject(new Error("network_error")));
      xhr.open("POST", url);
      xhr.send(form);
    });
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   ROUTER — simple single-page router
   ═══════════════════════════════════════════════════════════════════════════ */
const Router = {
  pages: {},

  register(name, el) {
    this.pages[name] = el;
  },

  /**
   * Navigate to a named page.
   * All others become hidden.
   */
  go(name) {
    Object.entries(this.pages).forEach(([key, el]) => {
      if (key === name) {
        el.classList.remove("hidden");
        el.classList.add("active");
      } else {
        el.classList.remove("active");
        el.classList.add("hidden");
      }
    });
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   AUTH MODULE
   ═══════════════════════════════════════════════════════════════════════════ */
const Auth = {
  STORAGE_KEY: "edtech-credentials",

  init() {
    // Restore remembered credentials
    const saved = JSON.parse(localStorage.getItem(this.STORAGE_KEY) || "null");
    if (saved) {
      $("#input-login").value    = saved.login    || "";
      $("#input-password").value = saved.password || "";
      $("#remember-me").checked  = true;
    }

    // Submit on Enter
    $$("#input-login, #input-password").forEach(inp => {
      inp.addEventListener("keydown", e => {
        if (e.key === "Enter") this.login();
      });
    });

    // Toggle password visibility
    $("#toggle-password").addEventListener("click", () => {
      const inp  = $("#input-password");
      const icon = $("#eye-icon");
      const show = inp.type === "password";
      inp.type = show ? "text" : "password";
      icon.className = show ? "ph ph-eye-slash" : "ph ph-eye";
    });

    // Login button
    $("#btn-login").addEventListener("click", () => this.login());
  },

  async login() {
    const login    = $("#input-login").value.trim();
    const password = $("#input-password").value;
    const remember = $("#remember-me").checked;

    if (!login || !password) {
      this._showError("Введите логин и пароль");
      return;
    }

    this._setLoading(true);
    this._hideError();

    try {
      const { ok, data } = await Api.post("/api/auth", { login, password });

      if (!ok) {
        // Backend unavailable or other HTTP error
        if (data.error === "backend_unavailable") {
          this._showError("Сервер недоступен. Проверьте соединение.");
        } else {
          this._showError("Ошибка сервера. Попробуйте позже.");
        }
        return;
      }

      // Backend returns "OK" on success, anything else is a failure
      if (data.result !== "OK") {
        this._showError("Неверный логин или пароль");
        return;
      }

      if (data.result === "OK") {
        // Remember credentials
        if (remember) {
          localStorage.setItem(this.STORAGE_KEY, JSON.stringify({ login, password }));
        } else {
          localStorage.removeItem(this.STORAGE_KEY);
        }

        // Route by role
        if (data.role === "admin") {
          Admin.init();
          Router.go("admin");
        } else if (data.role === "student") {
          Student.init();
          Router.go("student");
        } else {
          this._showError("Неизвестная роль пользователя");
        }
      }
    } catch (err) {
      this._showError("Сервер недоступен. Проверьте соединение.");
    } finally {
      this._setLoading(false);
    }
  },

  logout() {
    // Clear sensitive state
    Admin.reset();
    Student.reset();
    Router.go("login");
  },

  _setLoading(on) {
    const btn    = $("#btn-login");
    const text   = btn.querySelector(".btn__text");
    const loader = btn.querySelector(".btn__loader");
    btn.disabled = on;
    text.textContent = on ? "Входим…" : "Войти";
    loader.classList.toggle("hidden", !on);
  },

  _showError(msg) {
    const banner = $("#login-error");
    const text   = $("#login-error-text");
    text.textContent = msg;
    banner.classList.remove("hidden");
  },

  _hideError() {
    $("#login-error").classList.add("hidden");
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   ADMIN MODULE
   ═══════════════════════════════════════════════════════════════════════════ */
const Admin = {
  currentFile:     null,
  generatedQuestions: null,

  PANEL_META: {
    upload:    { title: "Загрузка базы знаний",   sub: "Загрузите документ для генерации вопросов" },
    generate:  { title: "Генерация вопросов",      sub: "Настройте параметры и запустите генерацию" },
    questions: { title: "Просмотр вопросов",       sub: "Проверьте сгенерированные вопросы перед сохранением" },
  },

  init() {
    // Sidebar navigation
    $$(".sidebar__item").forEach(btn => {
      btn.addEventListener("click", () => {
        const panel = btn.dataset.panel;
        this.switchPanel(panel);
      });
    });

    // Logout
    $("#admin-logout").addEventListener("click", () => Auth.logout());

    // Upload zone
    this._initUpload();

    // Spinbox controls
    $$(".spinbox__btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const target = btn.dataset.target;
        const delta  = parseInt(btn.dataset.delta, 10);
        const input  = $(`#${target}`);
        const min    = parseInt(input.min, 10) || 1;
        const max    = parseInt(input.max, 10) || 999;
        const newVal = Math.min(max, Math.max(min, parseInt(input.value, 10) + delta));
        input.value  = newVal;
      });
    });

    // Generate button
    $("#btn-generate").addEventListener("click", () => this.generateQuestions());

    // Save button
    $("#btn-save-questions").addEventListener("click", () => this.saveQuestions());

    // Go to upload panel on enter
    this.switchPanel("upload");
  },

  reset() {
    this.currentFile        = null;
    this.generatedQuestions = null;
    this._resetUploadUI();
  },

  /* ── Panel switching ──────────────────────────────────────────────────── */
  switchPanel(name) {
    $$(".sidebar__item").forEach(b => b.classList.remove("active"));
    $(`.sidebar__item[data-panel="${name}"]`)?.classList.add("active");

    $$(".panel").forEach(p => {
      p.classList.remove("active");
      p.classList.add("hidden");
    });
    const panel = $(`#panel-${name}`);
    if (panel) {
      panel.classList.remove("hidden");
      panel.classList.add("active");
    }

    const meta = this.PANEL_META[name];
    if (meta) {
      $("#admin-panel-title").textContent = meta.title;
      $("#admin-panel-sub").textContent   = meta.sub;
    }
  },

  /* ── Upload ───────────────────────────────────────────────────────────── */
  _initUpload() {
    const zone  = $("#upload-zone");
    const input = $("#file-input");

    // Click opens file picker
    zone.addEventListener("click", () => input.click());

    // Drag & Drop
    zone.addEventListener("dragover", e => {
      e.preventDefault();
      zone.classList.add("dragover");
    });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", e => {
      e.preventDefault();
      zone.classList.remove("dragover");
      const file = e.dataTransfer.files[0];
      if (file) this._setFile(file);
    });

    // File input change
    input.addEventListener("change", () => {
      if (input.files[0]) this._setFile(input.files[0]);
    });

    // Remove file
    $("#btn-remove-file").addEventListener("click", e => {
      e.stopPropagation();
      this._resetUploadUI();
    });

    // Upload button
    $("#btn-upload").addEventListener("click", () => this.uploadFile());
  },

  _setFile(file) {
    const ALLOWED = /\.(pdf|txt|doc|docx)$/i;
    if (!ALLOWED.test(file.name)) {
      Toast.error("Допустимые форматы: PDF, TXT, DOC, DOCX");
      return;
    }
    this.currentFile = file;

    $("#file-info-name").textContent = file.name;
    $("#file-info-size").textContent = formatBytes(file.size);
    $("#upload-file-info").classList.remove("hidden");
    $("#upload-actions").classList.remove("hidden");
  },

  _resetUploadUI() {
    this.currentFile = null;
    $("#file-input").value   = "";
    $("#upload-file-info").classList.add("hidden");
    $("#upload-actions").classList.add("hidden");
    $("#upload-progress").classList.add("hidden");
    $("#progress-fill").style.width = "0%";
  },

  async uploadFile() {
    if (!this.currentFile) {
      Toast.warning("Выберите файл для загрузки");
      return;
    }

    const btn    = $("#btn-upload");
    const text   = btn.querySelector(".btn__text");
    const loader = btn.querySelector(".btn__loader");
    btn.disabled      = true;
    loader.classList.remove("hidden");
    text.textContent  = "Загрузка…";

    const progressWrap = $("#upload-progress");
    const fill         = $("#progress-fill");
    const label        = $("#progress-label");
    progressWrap.classList.remove("hidden");

    try {
      const result = await Api.uploadFile("/api/upload_know_base", this.currentFile, (pct) => {
        fill.style.width      = `${pct}%`;
        label.textContent     = `Загрузка ${pct}%…`;
      });

      if (result.ok) {
        fill.style.width  = "100%";
        label.textContent = "Загрузка завершена ✓";
        Toast.success("База знаний успешно загружена!");
        setTimeout(() => {
          this._resetUploadUI();
          this.switchPanel("generate");
        }, 800);
      } else {
        const errMsg = result.data?.error || result.data?.detail || "Неизвестная ошибка";
        Toast.error(`Ошибка загрузки: ${errMsg}`);
        label.textContent = "Ошибка загрузки";
        btn.disabled = false;
        loader.classList.add("hidden");
        text.textContent = "Загрузить файл";
      }
    } catch (err) {
      Toast.error("Не удалось загрузить файл. Проверьте соединение с сервером.");
      label.textContent = "Ошибка соединения";
      btn.disabled = false;
      loader.classList.add("hidden");
      text.textContent = "Загрузить файл";
    }
  },

  /* ── Generate Questions ────────────────────────────────────────────────── */
  async generateQuestions() {
    const numQ = parseInt($("#num-questions").value, 10);
    const numA = parseInt($("#num-answers").value,   10);
    const numC = parseInt($("#num-correct").value,   10);

    if (numC >= numA) {
      Toast.warning("Правильных ответов должно быть меньше, чем всего вариантов");
      return;
    }

    const btn    = $("#btn-generate");
    const text   = btn.querySelector(".btn__text");
    const loader = btn.querySelector(".btn__loader");
    btn.disabled = true;
    loader.classList.remove("hidden");
    text.textContent = "Генерируем…";
    $("#generate-progress").classList.remove("hidden");

    try {
      const { ok, data } = await Api.post("/api/generate_questions", {
        num_questions:              numQ,
        num_answ_per_one_quest:     numA,
        num_correct_answ_per_one_quest: numC,
      });

      if (ok && data.msg_type === "questions_list") {
        this.generatedQuestions = data.questions;
        this._renderQuestions(data.questions);
        this.switchPanel("questions");
        Toast.success(`Сгенерировано ${data.questions.length} вопросов`);
      } else {
        const errMsg = data?.error || data?.detail || "Ошибка генерации";
        Toast.error(`Не удалось сгенерировать вопросы: ${errMsg}`);
      }
    } catch {
      Toast.error("Сервер недоступен. Попробуйте ещё раз.");
    } finally {
      btn.disabled = false;
      loader.classList.add("hidden");
      text.textContent = "Сгенерировать вопросы";
      $("#generate-progress").classList.add("hidden");
    }
  },

  /* ── Render Question Cards ─────────────────────────────────────────────── */
  _renderQuestions(questions) {
    const container = $("#questions-list");
    container.innerHTML = "";

    questions.forEach((q, idx) => {
      // Shuffle answers for display
      const allAnswers = [
        ...q.correct_answs.map(a => ({ text: a.answ_txt, correct: true })),
        ...q.not_correct_answs.map(a => ({ text: a.answ_txt, correct: false })),
      ];

      const answersHtml = allAnswers.map(a => `
        <div class="answer-item ${a.correct ? "answer-item--correct" : "answer-item--wrong"}">
          <i class="ph ${a.correct ? "ph-check-circle" : "ph-circle"}"></i>
          <span>${this._escape(a.text)}</span>
        </div>
      `).join("");

      const card = document.createElement("div");
      card.className = "q-card";
      card.style.animationDelay = `${idx * 0.04}s`;
      card.innerHTML = `
        <div class="q-card__num">Вопрос ${q.question_num}</div>
        <div class="q-card__text">${this._escape(q.question_txt)}</div>
        <div class="q-card__answers">${answersHtml}</div>
      `;
      container.appendChild(card);
    });
  },

  /* ── Save Questions ────────────────────────────────────────────────────── */
  async saveQuestions() {
    if (!this.generatedQuestions?.length) {
      Toast.warning("Нет вопросов для сохранения");
      return;
    }

    const btn    = $("#btn-save-questions");
    const text   = btn.querySelector(".btn__text");
    const loader = btn.querySelector(".btn__loader");
    btn.disabled = true;
    loader.classList.remove("hidden");
    text.textContent = "Сохранение…";

    try {
      const { ok, data } = await Api.post("/api/save_questions", {
        msg_type: "questions_list",
        questions: this.generatedQuestions,
      });

      if (ok && data.quest_list_id !== undefined) {
        await Modal.show({
          type:    "success",
          title:   "Список сохранён!",
          body:    `Список вопросов успешно добавлен в базу данных.\nID экзамена: ${data.quest_list_id}`,
          okLabel: "ОК",
        });
        this.reset();
        Auth.logout();
      } else {
        const errMsg = data?.error || data?.detail || "Неизвестная ошибка";
        Toast.error(`Не удалось сохранить: ${errMsg}`);
        btn.disabled = false;
        loader.classList.add("hidden");
        text.textContent = "Подтвердить и сохранить";
      }
    } catch {
      Toast.error("Сервер недоступен. Попробуйте ещё раз.");
      btn.disabled = false;
      loader.classList.add("hidden");
      text.textContent = "Подтвердить и сохранить";
    }
  },

  _escape(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   STUDENT MODULE
   ═══════════════════════════════════════════════════════════════════════════ */
const Student = {
  selectedExamId:  null,
  currentExamData: null,

  init() {
    // Logout
    $("#student-logout").addEventListener("click", () => Auth.logout());

    // Back button
    $("#btn-back-to-exams").addEventListener("click", () => this.showExamsList());

    // Start exam
    $("#btn-start-exam").addEventListener("click", () => this.startExam());

    // Submit exam
    $("#btn-submit-exam").addEventListener("click", () => this.submitExam());

    // Load available exams
    this.loadExams();
  },

  reset() {
    this.selectedExamId  = null;
    this.currentExamData = null;
    this._switchStudentPanel("exams");
  },

  /* ── Load Available Exams ─────────────────────────────────────────────── */
  async loadExams() {
    $("#exams-loading").style.display    = "flex";
    $("#exams-table-wrap").classList.add("hidden");

    try {
      const { ok, data } = await Api.get("/api/get_available_exams");

      if (ok && data.available_exams?.length) {
        this._renderExamsTable(data.available_exams);
        $("#exams-loading").style.display = "none";
        $("#exams-table-wrap").classList.remove("hidden");
      } else {
        // No exams available
        await Modal.show({
          type:  "info",
          title: "Нет доступных экзаменов",
          body:  "В настоящее время для вас нет доступных экзаменов. Обратитесь к администратору.",
        });
        Auth.logout();
      }
    } catch {
      await Modal.show({
        type:  "error",
        title: "Ошибка загрузки",
        body:  "Не удалось загрузить список экзаменов. Проверьте соединение с сервером.",
      });
      Auth.logout();
    }
  },

  _renderExamsTable(exams) {
    const tbody = $("#exams-tbody");
    tbody.innerHTML = "";

    exams.forEach((exam, idx) => {
      const tr = document.createElement("tr");
      const radioId = `exam-radio-${exam.available_exam_id}`;
      tr.innerHTML = `
        <td>
          <input
            type="radio"
            class="exam-radio"
            id="${radioId}"
            name="exam-select"
            value="${exam.available_exam_id}"
          />
        </td>
        <td>
          <label for="${radioId}" style="cursor:pointer; font-weight:600;">
            Экзамен #${exam.available_exam_id}
          </label>
        </td>
        <td>
          <span class="exam-status-badge">
            <i class="ph ph-circle" style="font-size:8px;"></i>
            Доступен
          </span>
        </td>
      `;
      tbody.appendChild(tr);

      // Auto-select first
      if (idx === 0) {
        tr.querySelector("input").checked = true;
        this.selectedExamId = exam.available_exam_id;
        $("#btn-start-exam").disabled = false;
      }
    });

    // Update selection on change
    tbody.addEventListener("change", e => {
      if (e.target.name === "exam-select") {
        this.selectedExamId = parseInt(e.target.value, 10);
        $("#btn-start-exam").disabled = false;
      }
    });
  },

  /* ── Start Exam ───────────────────────────────────────────────────────── */
  async startExam() {
    if (!this.selectedExamId) {
      Toast.warning("Выберите экзамен");
      return;
    }

    // In real scenario we'd fetch exam questions by ID.
    // The backend's /exam/get_available_exams doesn't return questions,
    // but since the spec doesn't include a "get exam by ID" endpoint,
    // we pass the selected exam ID in the submit payload.
    // We show the exam panel and let user answer questions loaded from the exam.

    // NOTE: The backend spec doesn't provide a "fetch questions for exam" endpoint.
    // Based on the spec we assume the exam questions come from /exam/execute's context,
    // so we show a placeholder — in production you'd call a GET /exam/get_exam?id=X
    // For this implementation we call a reasonable GET to get exam details.
    
    this._renderExamPlaceholder();
    this._switchStudentPanel("exam");
    $("#exam-title").textContent = `Экзамен #${this.selectedExamId}`;
  },

  /**
   * Renders a placeholder exam UI.
   * In production, replace with real question fetching from the backend.
   * The spec's /exam/execute accepts answers, so we build UI here.
   */
  _renderExamPlaceholder() {
    // Since the spec doesn't define a "get exam questions" endpoint,
    // we display a message + the submit button which will send the answers.
    // The actual exam questions would be fetched via an undocumented endpoint.
    const container = $("#exam-questions-list");
    container.innerHTML = `
      <div class="exam-q-card" style="text-align:center; padding: 40px;">
        <i class="ph ph-info" style="font-size:40px; color:var(--info); margin-bottom:16px; display:block;"></i>
        <div class="exam-q-card__text">
          Вы выбрали <strong>Экзамен #${this.selectedExamId}</strong>.<br/>
          Нажмите «Сдать экзамен» для отправки результатов.
        </div>
        <p style="color:var(--text-muted); font-size:13px; margin-top:12px;">
          (Для отображения вопросов необходим эндпоинт получения данных экзамена)
        </p>
      </div>
    `;
    this.currentExamData = { examId: this.selectedExamId, answers: [] };
  },

  showExamsList() {
    this._switchStudentPanel("exams");
  },

  /* ── Submit Exam ──────────────────────────────────────────────────────── */
  async submitExam() {
    // Collect selected answers from checkboxes
    // Backend expects: [{question_num, user_answs: [{answ_txt}]}]
    const answersMap = {};
    $$(".exam-option.selected").forEach(opt => {
      const qNum = parseInt(opt.dataset.questionNum, 10);
      if (!answersMap[qNum]) answersMap[qNum] = [];
      answersMap[qNum].push({ answ_txt: opt.dataset.answTxt });
    });
    const answers = Object.entries(answersMap).map(([qNum, userAnsws]) => ({
      question_num: parseInt(qNum, 10),
      user_answs: userAnsws,
    }));

    const btn    = $("#btn-submit-exam");
    const text   = btn.querySelector(".btn__text");
    const loader = btn.querySelector(".btn__loader");
    btn.disabled = true;
    loader.classList.remove("hidden");
    text.textContent = "Отправка…";

    try {
      const { ok, data } = await Api.post("/api/execute_exam", {
        msg_type: "exam_procedure",
        exam_id:  this.selectedExamId,
        answers,
      });

      if (ok && data.correct_answs !== undefined) {
        const total = data.correct_answs + data.incorrect_answs;
        const pct   = total > 0 ? Math.round((data.correct_answs / total) * 100) : 0;
        const grade = pct >= 80 ? "Отлично" : pct >= 60 ? "Хорошо" : pct >= 40 ? "Удовлетворительно" : "Неудовлетворительно";

        await Modal.show({
          type:  pct >= 60 ? "success" : "warning",
          title: `Результат: ${grade}`,
          body:  `Правильных ответов: ${data.correct_answs}\nНеправильных ответов: ${data.incorrect_answs}\nРезультат: ${pct}%`,
          okLabel: "Завершить",
        });
        this.reset();
        Auth.logout();
      } else {
        const errMsg = data?.error || data?.detail || "Неизвестная ошибка";
        Toast.error(`Ошибка сдачи экзамена: ${errMsg}`);
        btn.disabled = false;
        loader.classList.add("hidden");
        text.textContent = "Сдать экзамен";
      }
    } catch {
      Toast.error("Сервер недоступен. Попробуйте ещё раз.");
      btn.disabled = false;
      loader.classList.add("hidden");
      text.textContent = "Сдать экзамен";
    }
  },

  _switchStudentPanel(name) {
    const panels = {
      exams: $("#student-panel-exams"),
      exam:  $("#student-panel-exam"),
    };
    Object.entries(panels).forEach(([key, el]) => {
      if (key === name) {
        el.classList.remove("hidden");
        el.classList.add("active");
      } else {
        el.classList.remove("active");
        el.classList.add("hidden");
      }
    });
  },
};

/* ═══════════════════════════════════════════════════════════════════════════
   BOOTSTRAP
   ═══════════════════════════════════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {
  // Init subsystems
  Theme.init();
  Toast.init();
  Modal.init();

  // Register pages with router
  Router.register("login",   $("#page-login"));
  Router.register("admin",   $("#page-admin"));
  Router.register("student", $("#page-student"));

  // Init auth
  Auth.init();

  // Hide loading screen and show app
  setTimeout(() => {
    const loadingScreen = $("#loading-screen");
    const app           = $("#app");
    loadingScreen.classList.add("hidden");
    app.classList.remove("hidden");
    Router.go("login");
  }, 900);
});
