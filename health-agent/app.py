"""Sehat - personal health agent. FastAPI server.

Run from this directory:  uvicorn app:app --reload
Then open http://localhost:8000

Requires a local Ollama instance ('ollama serve') with the model pulled
(default llama3.2, override with HEALTH_AGENT_MODEL / OLLAMA_URL env vars).
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import agent
import database as db

db.init_db()

app = FastAPI(title="Sehat - Personal Health Agent")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    text = req.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty message")
    try:
        reply, logged = agent.chat(text)
    except agent.OllamaUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))
    return {"reply": reply, "logged": logged}


@app.get("/api/dashboard")
def dashboard():
    today = db.day_totals()
    return {
        "profile": db.get_profile(),
        "today": today,
        "week": db.last_n_days(7),
        "weights": db.weight_history(30),
        "streak_days": db.streak_days(),
        "checklist": {
            "water": today["water_glasses"] >= 8,
            "meals": today["meals_logged"] >= 2,
            "movement": today["workout_min"] >= 20,
            "mood": today["mood"] is not None,
            "sleep": today["sleep_hours"] is not None,
        },
    }


@app.get("/api/history")
def history():
    return {"messages": db.recent_messages(50)}


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
