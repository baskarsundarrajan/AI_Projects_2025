/* Sehat frontend: dashboard rendering + chat. Vanilla JS, no build step. */

const $ = (id) => document.getElementById(id);
const tooltip = $("tooltip");

const SERIES = {
  water: { color: "var(--c-water)", max: 10, unit: "glasses", key: "water_glasses" },
  sleep: { color: "var(--c-sleep)", max: 12, unit: "hrs", key: "sleep_hours" },
  mood:  { color: "var(--c-mood)",  max: 5,  unit: "/5",  key: "mood" },
};

const CHECK_ITEMS = [
  ["water", "8 glasses of water"],
  ["meals", "Meals logged"],
  ["movement", "20+ min movement"],
  ["mood", "Mood check-in"],
  ["sleep", "Sleep logged"],
];

function dayName(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString(undefined, { weekday: "short" });
}

function showTip(e, text) {
  tooltip.textContent = text;
  tooltip.hidden = false;
  tooltip.style.left = Math.min(e.clientX + 12, window.innerWidth - 160) + "px";
  tooltip.style.top = (e.clientY - 34) + "px";
}
function hideTip() { tooltip.hidden = true; }

/* ---------- dashboard ---------- */

async function refreshDashboard() {
  let data;
  try {
    data = await (await fetch("/api/dashboard")).json();
  } catch {
    return; // server hiccup; keep last render
  }

  $("streak-days").textContent = data.streak_days;
  $("t-water").textContent = data.today.water_glasses;
  $("t-move").textContent = data.today.workout_min;
  $("t-cal").textContent = data.today.calories;
  $("t-sleep").textContent = data.today.sleep_hours ?? "—";

  const list = $("checklist");
  list.innerHTML = "";
  for (const [key, label] of CHECK_ITEMS) {
    const li = document.createElement("li");
    const done = data.checklist[key];
    li.className = done ? "done" : "";
    li.innerHTML = `<span class="mark">${done ? "✓" : "○"}</span>${label}`;
    list.appendChild(li);
  }

  for (const name of ["water", "sleep", "mood"]) {
    renderBars($("chart-" + name), name, data.week);
  }
  renderWeight($("chart-weight"), data.weights);
}

function renderBars(el, name, week) {
  const spec = SERIES[name];
  el.innerHTML = "";
  const values = week.map((d) => d[spec.key]);
  const peak = Math.max(spec.max, ...values.filter((v) => v != null));

  week.forEach((d, i) => {
    const v = values[i];
    const col = document.createElement("div");
    col.className = "col" + (i === week.length - 1 && v != null ? " labeled" : "");
    const val = document.createElement("div");
    val.className = "val";
    val.textContent = v ?? "";
    const bar = document.createElement("div");
    bar.className = "bar" + (v == null || v === 0 ? " empty" : "");
    const h = v ? Math.max(4, (v / peak) * 88) : 2;
    bar.style.height = h + "px";
    if (v) bar.style.background = spec.color;
    col.append(val, bar);
    col.addEventListener("mousemove", (e) =>
      showTip(e, `${dayName(d.day)}: ${v ?? "not logged"}${v != null ? " " + spec.unit : ""}`));
    col.addEventListener("mouseleave", hideTip);
    el.appendChild(col);
  });

  let labels = el.parentElement.querySelector(".daylabels");
  if (!labels) {
    labels = document.createElement("div");
    labels.className = "daylabels";
    el.parentElement.appendChild(labels);
  }
  labels.innerHTML = week.map((d) => `<span>${dayName(d.day)}</span>`).join("");
}

function renderWeight(el, weights) {
  if (!weights.length) {
    el.innerHTML = '<div class="no-data">No weight entries yet — tell Sehat your weight to start the trend.</div>';
    return;
  }
  const W = el.clientWidth || 280, H = 130, pad = { t: 14, r: 34, b: 18, l: 8 };
  const vals = weights.map((w) => w.weight_kg);
  const min = Math.min(...vals), max = Math.max(...vals);
  const span = max - min || 1;
  const x = (i) => pad.l + (weights.length === 1 ? (W - pad.l - pad.r) / 2
    : (i / (weights.length - 1)) * (W - pad.l - pad.r));
  const y = (v) => pad.t + (1 - (v - min) / span) * (H - pad.t - pad.b);

  const pts = weights.map((w, i) => `${x(i)},${y(w.weight_kg)}`).join(" ");
  const last = weights[weights.length - 1];
  const svgNS = "http://www.w3.org/2000/svg";
  el.innerHTML = "";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);

  const base = document.createElementNS(svgNS, "line");
  base.setAttribute("x1", pad.l); base.setAttribute("x2", W - pad.r);
  base.setAttribute("y1", H - pad.b); base.setAttribute("y2", H - pad.b);
  base.setAttribute("stroke", "var(--baseline)");
  svg.appendChild(base);

  const line = document.createElementNS(svgNS, "polyline");
  line.setAttribute("points", pts);
  line.setAttribute("fill", "none");
  line.setAttribute("stroke", "var(--c-weight)");
  line.setAttribute("stroke-width", "2");
  line.setAttribute("stroke-linejoin", "round");
  svg.appendChild(line);

  weights.forEach((w, i) => {
    const dot = document.createElementNS(svgNS, "circle");
    dot.setAttribute("cx", x(i)); dot.setAttribute("cy", y(w.weight_kg));
    dot.setAttribute("r", i === weights.length - 1 ? 4 : 3);
    dot.setAttribute("fill", "var(--c-weight)");
    dot.setAttribute("stroke", "var(--surface)");
    dot.setAttribute("stroke-width", "2");
    const hit = document.createElementNS(svgNS, "circle"); // bigger hover target
    hit.setAttribute("cx", x(i)); hit.setAttribute("cy", y(w.weight_kg));
    hit.setAttribute("r", 9); hit.setAttribute("fill", "transparent");
    hit.addEventListener("mousemove", (e) => showTip(e, `${w.day}: ${w.weight_kg} kg`));
    hit.addEventListener("mouseleave", hideTip);
    svg.append(dot, hit);
  });

  const label = document.createElementNS(svgNS, "text"); // direct label on last point
  label.setAttribute("x", x(weights.length - 1) + 7);
  label.setAttribute("y", y(last.weight_kg) + 4);
  label.setAttribute("fill", "var(--ink-2)");
  label.setAttribute("font-size", "11");
  label.textContent = `${last.weight_kg}`;
  svg.appendChild(label);

  el.appendChild(svg);
}

/* ---------- chat ---------- */

const messagesEl = $("messages");
const form = $("chat-form");
const input = $("chat-input");
const sendBtn = $("chat-send");

function addMsg(role, text, cls = "") {
  const div = document.createElement("div");
  div.className = `msg ${role} ${cls}`.trim();
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function addLoggedChips(logged) {
  if (!logged || !logged.length) return;
  const div = document.createElement("div");
  div.className = "logged-chips";
  div.innerHTML = logged
    .map((l) => `<span>✓ ${l.tool.replace("log_", "").replace("update_", "").replace("_", " ")} saved</span>`)
    .join("");
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function loadHistory() {
  try {
    const data = await (await fetch("/api/history")).json();
    for (const m of data.messages) addMsg(m.role === "user" ? "user" : "agent", m.content);
  } catch { /* fresh start */ }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text || sendBtn.disabled) return;
  input.value = "";
  addMsg("user", text);
  sendBtn.disabled = true;
  const typing = addMsg("agent", "thinking…", "typing");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    typing.remove();
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      addMsg("agent", err.detail || `Something went wrong (HTTP ${res.status}).`, "error");
    } else {
      const data = await res.json();
      addLoggedChips(data.logged);
      addMsg("agent", data.reply);
      if (data.logged.length) refreshDashboard();
    }
  } catch {
    typing.remove();
    addMsg("agent", "Could not reach the server — is uvicorn still running?", "error");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});

loadHistory();
refreshDashboard();
setInterval(refreshDashboard, 60_000);
