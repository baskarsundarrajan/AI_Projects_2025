"""The agent loop: talks to a local Ollama model with tool-calling.

Flow per user message:
  1. Build context: system prompt + profile + today's totals + recent chat history.
  2. Send to Ollama /api/chat with the tool schemas.
  3. If the model calls tools, execute them and loop back with the results.
  4. Return the final text reply plus a list of what got logged.
"""

import json
import os

import requests

import database as db
from health_tools import TOOLS, execute_tool

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("HEALTH_AGENT_MODEL", "llama3.2")
MAX_TOOL_ROUNDS = 5
HISTORY_LIMIT = 30

SYSTEM_PROMPT = """You are Sehat, a warm and practical personal health companion. You help one user \
with diet, fitness, mental wellness, and daily habits (water, sleep, medication, streaks).

Core behaviours:
- When the user mentions something loggable (a meal, exercise, mood, water, sleep, weight), \
call the matching log tool. Estimate calories for meals yourself when not given; Indian home \
food is common. Then respond naturally - confirm briefly, don't repeat the data back verbatim.
- When they share a lasting fact about themselves (age, goal, diet preference, condition), \
save it with update_profile.
- When asked about progress or trends ("how am I doing?", "did I sleep enough this week?"), \
call get_history first, then answer from the actual data - cite specifics.
- Be encouraging but honest. Short replies. One question at a time, never a survey.
- If profile is empty, get to know the user gradually through conversation, not a questionnaire.

Boundaries:
- You are not a doctor. For symptoms, medication changes, or anything clinical, give general \
guidance only and recommend a professional.
- If the user expresses thoughts of self-harm or severe distress, respond with care and urge \
them to reach out to a helpline or someone they trust (in India: Tele-MANAS 14416).\
"""


class OllamaUnavailable(Exception):
    pass


def _context_block():
    profile = db.get_profile()
    today = db.day_totals()
    parts = ["\n\n--- Current context (from your database, do not mention this block) ---"]
    parts.append("User profile: " + (json.dumps(profile) if profile else "empty - you don't know this user yet"))
    parts.append("Today so far: " + json.dumps(today))
    parts.append(f"Logging streak: {db.streak_days()} days")
    return "\n".join(parts)


def _call_ollama(messages):
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "tools": TOOLS, "stream": False},
            timeout=180,
        )
    except requests.exceptions.ConnectionError:
        raise OllamaUnavailable(
            f"Cannot reach Ollama at {OLLAMA_URL}. Start it with 'ollama serve' "
            f"and make sure the model is pulled: 'ollama pull {MODEL}'."
        )
    r.raise_for_status()
    return r.json()["message"]


def chat(user_message):
    """Run one full agent turn. Returns (reply_text, logged_events)."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT + _context_block()}]
    messages += db.recent_messages(HISTORY_LIMIT)
    messages.append({"role": "user", "content": user_message})

    logged = []
    reply = ""
    for _ in range(MAX_TOOL_ROUNDS):
        msg = _call_ollama(messages)
        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            reply = msg.get("content", "").strip()
            break
        messages.append(msg)
        for call in tool_calls:
            fn = call.get("function", {})
            name = fn.get("name", "")
            args = fn.get("arguments") or {}
            if isinstance(args, str):  # some models return arguments as a JSON string
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            result = execute_tool(name, args)
            if "error" not in result and name != "get_history":
                logged.append({"tool": name, "args": args})
            messages.append({"role": "tool", "content": json.dumps(result)})
    else:
        reply = "I logged what you told me, but got stuck composing a reply - mind rephrasing?"

    if not reply:
        reply = "Noted!" if logged else "Sorry, I didn't produce a reply - could you rephrase?"
    # persist only after a successful turn, so a dead Ollama doesn't leave
    # unanswered messages in the history
    db.save_message("user", user_message)
    db.save_message("assistant", reply)
    return reply, logged
