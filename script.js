const pw = document.getElementById("pw");
const toggle = document.getElementById("toggle");
const bars = document.querySelectorAll(".meter span");
const verdict = document.getElementById("verdict");
const lenEl = document.getElementById("len");
const entEl = document.getElementById("ent");
const crackEl = document.getElementById("crack");
const tips = document.getElementById("tips");
const rules = document.querySelectorAll("#rules li");

const LEVELS = [
  { label: "Very weak", color: "#ff6b6b" },
  { label: "Weak", color: "#ff9f43" },
  { label: "Fair", color: "#fbd34d" },
  { label: "Strong", color: "#86e07a" },
  { label: "Very strong", color: "#6ee7a0" }
];

const COMMON = ["password", "123456", "qwerty", "letmein", "admin", "welcome", "iloveyou", "monkey", "dragon", "abc123", "football", "login", "111111"];
const PATTERNS = ["abcdef", "qwerty", "asdfgh", "zxcvbn", "123456", "654321", "987654"];

function isCommon(p) {
  const s = p.toLowerCase();
  if (COMMON.some(w => s.includes(w))) return true;
  if (PATTERNS.some(w => s.includes(w))) return true;
  if (/^(.)\1+$/.test(p)) return true;
  return false;
}

function poolSize(p) {
  let pool = 0;
  if (/[a-z]/.test(p)) pool += 26;
  if (/[A-Z]/.test(p)) pool += 26;
  if (/\d/.test(p)) pool += 10;
  if (/[^A-Za-z0-9]/.test(p)) pool += 32;
  return pool;
}

function entropyBits(p) {
  if (!p) return 0;
  let bits = p.length * Math.log2(poolSize(p));
  const repeats = p.length - new Set(p).size;
  bits -= repeats * 1.5;
  if (isCommon(p)) bits = Math.min(bits, 20);
  return Math.max(0, bits);
}

function crackTime(bits) {
  if (bits === 0) return "-";
  const guessesPerSecond = 1e10;
  const seconds = Math.pow(2, bits) / 2 / guessesPerSecond;
  if (seconds < 1) return "Instantly";
  const units = [["year", 31536000], ["day", 86400], ["hour", 3600], ["minute", 60], ["second", 1]];
  if (seconds > 31536000 * 1e6) return "Millions of years+";
  for (const [name, size] of units) {
    if (seconds >= size) {
      const n = Math.round(seconds / size);
      return n.toLocaleString() + " " + name + (n === 1 ? "" : "s");
    }
  }
  return "Instantly";
}

function check(p) {
  return {
    length: p.length >= 12,
    lower: /[a-z]/.test(p),
    upper: /[A-Z]/.test(p),
    number: /\d/.test(p),
    symbol: /[^A-Za-z0-9]/.test(p),
    common: p.length > 0 && !isCommon(p)
  };
}

function levelFor(bits, p) {
  if (!p) return -1;
  if (bits < 28) return 0;
  if (bits < 40) return 1;
  if (bits < 60) return 2;
  if (bits < 80) return 3;
  return 4;
}

function update() {
  const p = pw.value;
  const result = check(p);
  rules.forEach(li => li.classList.toggle("ok", result[li.dataset.rule]));
  const bits = entropyBits(p);
  const level = levelFor(bits, p);
  bars.forEach((bar, i) => {
    bar.style.background = i <= level ? LEVELS[level].color : "";
  });
  lenEl.textContent = p.length;
  entEl.textContent = Math.round(bits) + " bits";
  crackEl.textContent = crackTime(bits);
  if (level === -1) {
    verdict.textContent = "Start typing to see your score";
    verdict.style.color = "";
    tips.textContent = "";
    return;
  }
  verdict.textContent = LEVELS[level].label;
  verdict.style.color = LEVELS[level].color;
  const missing = Object.keys(result).filter(k => !result[k]);
  const hints = {
    length: "Use 12 or more characters.",
    lower: "Add a lowercase letter.",
    upper: "Add an uppercase letter.",
    number: "Add a number.",
    symbol: "Add a symbol.",
    common: "Avoid common words and keyboard patterns."
  };
  tips.textContent = missing.length ? hints[missing[0]] : "Nice. Use a unique password for every account.";
}

toggle.addEventListener("click", () => {
  const show = pw.type === "password";
  pw.type = show ? "text" : "password";
  toggle.textContent = show ? "Hide" : "Show";
  toggle.setAttribute("aria-pressed", String(show));
});
pw.addEventListener("input", update);
update();
