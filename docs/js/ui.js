/* Shared page helpers: DOM building, dates, theme, heatmap, next-up. */
"use strict";

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
}

function fmtDate(ts) {
  return new Date(ts).toLocaleDateString(undefined, {
    month: "short", day: "numeric",
  });
}

function fmtWhen(ts) {
  return new Date(ts).toLocaleString(undefined, {
    month: "short", day: "numeric", hour: "numeric", minute: "2-digit",
  });
}

function asOf(state) {
  const n = document.getElementById("asof");
  if (!n) return;
  n.textContent = state.events.length
    ? "progress as of " + fmtWhen(state.events[state.events.length - 1].ts) +
      " (this page reads the committed log - a fresh push shows up on the " +
      "public site within ~10 minutes)"
    : "no progress recorded yet - the first win takes about five minutes";
}

/* theme: system by default; the button cycles an explicit choice */
(function themeInit() {
  let saved = null;
  try { saved = localStorage.getItem("codin-theme"); } catch (e) {}
  if (saved) document.documentElement.dataset.theme = saved;
  window.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("themeBtn");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const cur = document.documentElement.dataset.theme;
      const next = cur === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("codin-theme", next); } catch (e) {}
    });
  });
})();

/* days: ["YYYY-MM-DD", ...] -> heatmap grid of the last `weeks` weeks */
function heatmap(days, weeks) {
  const set = new Set(days);
  const wrap = el("div", "heat-wrap");
  const grid = el("div", "heat");
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const start = new Date(today);
  // back to this week's Monday, then (weeks-1) whole weeks further
  start.setDate(start.getDate() - ((today.getDay() + 6) % 7) - (weeks - 1) * 7);
  const d = new Date(start);
  for (let w = 0; w < weeks; w++) {
    const col = el("div", "wk");
    for (let i = 0; i < 7; i++) {
      const key = d.toISOString().slice(0, 10);
      const future = d > today;
      const cell = el("i", !future && set.has(key) ? "on" : "");
      if (future) cell.style.visibility = "hidden";
      cell.title = key;
      col.appendChild(cell);
      d.setDate(d.getDate() + 1);
    }
    grid.appendChild(col);
  }
  wrap.appendChild(grid);
  return wrap;
}

/* the dashboard's next-up: first undone exercise of the first unlocked
 * module (in-progress modules first). Mirrors the CLI's spirit, not its
 * every rule - the CLI is the authority. */
function nextUp(curriculum, state) {
  const met = (reqs) => reqs.every((r) =>
    state.completed_modules.indexOf(r) >= 0 || state.done[r]);
  const mods = curriculum.modules.filter((m) => m.exercises.length);
  const score = (m) => {
    const done = m.exercises.filter((e) => state.done[e.id]).length;
    return done > 0 && done < m.exercises.length ? 0 : 1;
  };
  mods.sort((a, b) => score(a) - score(b));
  for (const m of mods) {
    if (!met(m.requires)) continue;
    for (const ex of m.exercises) {
      if (!state.done[ex.id] && met(ex.requires || [])) {
        return { module: m, ex };
      }
    }
  }
  return null;
}

function daysSinceLast(state) {
  if (!state.events.length) return null;
  const last = state.events[state.events.length - 1].ts;
  return Math.floor((Date.now() - Date.parse(last)) / 86400000);
}
