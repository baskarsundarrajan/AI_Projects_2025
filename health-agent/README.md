# Sehat — Personal Health Agent

A single-user health companion that runs entirely on your machine. You talk to it
in plain language — *"had poha for breakfast"*, *"walked 30 minutes"*, *"feeling
low today"*, *"slept 6 hours"* — and it logs everything, remembers you across
days, and answers questions about your trends from your actual data.

Covers **diet & nutrition, fitness & activity, mental wellness, and daily habits**
(water, sleep, streaks) in one place, with a live dashboard next to the chat.

## How it works

- **LLM**: local [Ollama](https://ollama.com) model (default `llama3.2`) with
  **tool calling** — the model decides when to call `log_meal`, `log_workout`,
  `log_mood`, `log_water`, `log_sleep`, `log_weight`, `update_profile`, or
  `get_history`, and the server executes them against the database.
- **Memory**: SQLite (`health_agent.db`, created on first run, not committed).
  Stores your profile, all daily logs, and chat history, so the agent knows you
  across restarts.
- **UI**: one FastAPI server serving a static HTML/JS page — chat panel plus a
  dashboard with today's checklist, streak, 7-day water/sleep/mood charts, and a
  weight trend. No npm, no build step.

## Setup

1. Install [Ollama](https://ollama.com) and pull the model:

   ```bash
   ollama pull llama3.2
   ollama serve   # if not already running
   ```

2. Install Python deps (Python 3.10+):

   ```bash
   pip install -r requirements.txt
   ```

3. Run from this directory:

   ```bash
   uvicorn app:app --reload
   ```

4. Open <http://localhost:8000> and start talking.

## Configuration (env vars, all optional)

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434` | Where Ollama is listening |
| `HEALTH_AGENT_MODEL` | `llama3.2` | Any tool-calling-capable Ollama model (e.g. `qwen2.5:7b` for better reasoning) |
| `HEALTH_AGENT_DB` | `./health_agent.db` | SQLite file location |

## Layout

```
app.py           FastAPI server: /api/chat, /api/dashboard, /api/history, static UI
agent.py         Agent loop: context building + Ollama tool-calling rounds
health_tools.py  Tool schemas the model sees + their implementations
database.py      SQLite schema, logging, and summary/streak queries
static/          index.html, style.css, app.js (vanilla JS, light/dark aware)
```

## Notes & limits

- Single user, no auth — meant for localhost use only. Don't expose it to a network.
- Calorie counts are the model's estimates, not measurements.
- It is **not a doctor**: it declines clinical advice and points to professionals;
  for severe distress it surfaces India's Tele-MANAS helpline (14416).
- Small models (3B) occasionally miss a log or mangle a tool call — the UI shows
  "✓ … saved" chips for what was actually written, so you can tell. A larger
  model via `HEALTH_AGENT_MODEL` improves this.
