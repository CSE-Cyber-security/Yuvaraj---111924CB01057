(function () {
  "use strict";

  const STORAGE_KEY = "todo-list-tasks";

  const els = {
    date: document.getElementById("today-date"),
    form: document.getElementById("task-form"),
    input: document.getElementById("task-input"),
    error: document.getElementById("form-error"),
    list: document.getElementById("task-list"),
    empty: document.getElementById("empty-state"),
    summary: document.getElementById("summary"),
    clear: document.getElementById("clear-completed"),
    filters: document.querySelectorAll(".filter"),
    counts: {
      all: document.getElementById("count-all"),
      pending: document.getElementById("count-pending"),
      completed: document.getElementById("count-completed"),
    },
  };

  let tasks = loadTasks();
  let filter = "all";

  /* ---------- Storage ---------- */

  function loadTasks() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
      if (!Array.isArray(saved)) return [];
      return saved.filter(
        (t) => t && typeof t.id === "string" && typeof t.text === "string"
      );
    } catch (err) {
      return [];
    }
  }

  function saveTasks() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    } catch (err) {
      // Storage can be unavailable (private mode, full quota).
      // The app still works for the current session.
    }
  }

  /* ---------- Actions ---------- */

  function createId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function addTask(text) {
    tasks.unshift({ id: createId(), text: text, done: false });
    saveTasks();
    render();
  }

  function toggleTask(id) {
    const task = tasks.find((t) => t.id === id);
    if (!task) return;
    task.done = !task.done;
    saveTasks();
    render();
  }

  function deleteTask(id) {
    tasks = tasks.filter((t) => t.id !== id);
    saveTasks();
    render();
  }

  function clearCompleted() {
    tasks = tasks.filter((t) => !t.done);
    saveTasks();
    render();
  }

  /* ---------- Rendering ---------- */

  function visibleTasks() {
    if (filter === "pending") return tasks.filter((t) => !t.done);
    if (filter === "completed") return tasks.filter((t) => t.done);
    return tasks;
  }

  function buildItem(task) {
    const li = document.createElement("li");
    li.className = "task" + (task.done ? " is-done" : "");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "task-check";
    checkbox.id = "task-" + task.id;
    checkbox.checked = task.done;
    checkbox.addEventListener("change", () => toggleTask(task.id));

    const label = document.createElement("label");
    label.className = "task-text";
    label.htmlFor = checkbox.id;
    label.textContent = task.text; // textContent keeps user input safe from HTML injection

    const del = document.createElement("button");
    del.type = "button";
    del.className = "icon-button";
    del.textContent = "×";
    del.setAttribute("aria-label", "Delete task: " + task.text);
    del.addEventListener("click", () => deleteTask(task.id));

    li.append(checkbox, label, del);
    return li;
  }

  function emptyMessage() {
    if (tasks.length === 0) return "No tasks yet. Add your first one above.";
    if (filter === "pending") return "Nothing pending. Enjoy the quiet.";
    if (filter === "completed") return "Nothing finished yet. Check off a task when it's done.";
    return "";
  }

  function summaryText(pending, total) {
    if (total === 0) return "";
    if (pending === 0) return "Everything is done.";
    if (pending === 1) return "1 task left.";
    return pending + " tasks left.";
  }

  function render() {
    const total = tasks.length;
    const done = tasks.filter((t) => t.done).length;
    const pending = total - done;

    els.counts.all.textContent = total;
    els.counts.pending.textContent = pending;
    els.counts.completed.textContent = done;

    const shown = visibleTasks();
    els.list.replaceChildren(...shown.map(buildItem));

    if (shown.length === 0) {
      els.empty.textContent = emptyMessage();
      els.empty.hidden = false;
    } else {
      els.empty.hidden = true;
    }

    els.summary.textContent = summaryText(pending, total);
    els.clear.disabled = done === 0;
  }

  /* ---------- Events ---------- */

  els.form.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = els.input.value.trim().replace(/\s+/g, " ");

    if (!text) {
      els.error.hidden = false;
      els.input.setAttribute("aria-invalid", "true");
      els.input.focus();
      return;
    }

    addTask(text);
    els.input.value = "";
    els.input.focus();
  });

  els.input.addEventListener("input", () => {
    els.error.hidden = true;
    els.input.removeAttribute("aria-invalid");
  });

  els.filters.forEach((button) => {
    button.addEventListener("click", () => {
      filter = button.dataset.filter;
      els.filters.forEach((b) => {
        const active = b === button;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-pressed", String(active));
      });
      render();
    });
  });

  els.clear.addEventListener("click", clearCompleted);

  /* ---------- Init ---------- */

  els.date.textContent = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  render();
})();
