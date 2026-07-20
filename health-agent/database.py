"""SQLite persistence for the health agent.

Single-user, file-based. The DB lives next to the code (health_agent.db,
gitignored) so the agent remembers profile, daily logs, and chat history
across restarts.
"""

import os
import sqlite3
from datetime import date, datetime, timedelta

DB_PATH = os.getenv("HEALTH_AGENT_DB", os.path.join(os.path.dirname(__file__), "health_agent.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    description TEXT NOT NULL,
    calories INTEGER
);
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    activity TEXT NOT NULL,
    duration_min INTEGER NOT NULL,
    intensity TEXT
);
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    rating INTEGER NOT NULL,
    note TEXT
);
CREATE TABLE IF NOT EXISTS water (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    glasses INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS sleep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL UNIQUE,
    hours REAL NOT NULL,
    quality TEXT
);
CREATE TABLE IF NOT EXISTS weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL UNIQUE,
    weight_kg REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL
);
"""


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.executescript(SCHEMA)


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _today():
    return date.today().isoformat()


# ---------- profile ----------

def set_profile(key, value):
    with _conn() as conn:
        conn.execute(
            "INSERT INTO profile (key, value, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
            (key, str(value), _now()),
        )


def get_profile():
    with _conn() as conn:
        rows = conn.execute("SELECT key, value FROM profile").fetchall()
    return {r["key"]: r["value"] for r in rows}


# ---------- logging ----------

def log_meal(description, calories=None):
    with _conn() as conn:
        conn.execute("INSERT INTO meals (ts, description, calories) VALUES (?, ?, ?)",
                     (_now(), description, calories))


def log_workout(activity, duration_min, intensity=None):
    with _conn() as conn:
        conn.execute("INSERT INTO workouts (ts, activity, duration_min, intensity) VALUES (?, ?, ?, ?)",
                     (_now(), activity, int(duration_min), intensity))


def log_mood(rating, note=None):
    with _conn() as conn:
        conn.execute("INSERT INTO moods (ts, rating, note) VALUES (?, ?, ?)",
                     (_now(), int(rating), note))


def log_water(glasses=1):
    with _conn() as conn:
        conn.execute("INSERT INTO water (ts, glasses) VALUES (?, ?)", (_now(), int(glasses)))


def log_sleep(hours, quality=None, day=None):
    day = day or _today()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO sleep (day, hours, quality) VALUES (?, ?, ?) "
            "ON CONFLICT(day) DO UPDATE SET hours=excluded.hours, quality=excluded.quality",
            (day, float(hours), quality),
        )


def log_weight(weight_kg, day=None):
    day = day or _today()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO weights (day, weight_kg) VALUES (?, ?) "
            "ON CONFLICT(day) DO UPDATE SET weight_kg=excluded.weight_kg",
            (day, float(weight_kg)),
        )


# ---------- chat history ----------

def save_message(role, content):
    with _conn() as conn:
        conn.execute("INSERT INTO messages (ts, role, content) VALUES (?, ?, ?)",
                     (_now(), role, content))


def recent_messages(limit=30):
    with _conn() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


# ---------- summaries ----------

def _day_of(ts):
    return ts[:10]


def day_totals(day=None):
    """Aggregate everything logged on one day."""
    day = day or _today()
    like = day + "%"
    with _conn() as conn:
        water = conn.execute("SELECT COALESCE(SUM(glasses),0) n FROM water WHERE ts LIKE ?", (like,)).fetchone()["n"]
        calories = conn.execute("SELECT COALESCE(SUM(calories),0) n FROM meals WHERE ts LIKE ?", (like,)).fetchone()["n"]
        meals = conn.execute("SELECT COUNT(*) n FROM meals WHERE ts LIKE ?", (like,)).fetchone()["n"]
        workout_min = conn.execute("SELECT COALESCE(SUM(duration_min),0) n FROM workouts WHERE ts LIKE ?", (like,)).fetchone()["n"]
        mood = conn.execute("SELECT rating FROM moods WHERE ts LIKE ? ORDER BY id DESC LIMIT 1", (like,)).fetchone()
        sleep_row = conn.execute("SELECT hours FROM sleep WHERE day = ?", (day,)).fetchone()
    return {
        "day": day,
        "water_glasses": water,
        "calories": calories,
        "meals_logged": meals,
        "workout_min": workout_min,
        "mood": mood["rating"] if mood else None,
        "sleep_hours": sleep_row["hours"] if sleep_row else None,
    }


def last_n_days(n=7):
    today = date.today()
    return [day_totals((today - timedelta(days=i)).isoformat()) for i in range(n - 1, -1, -1)]


def weight_history(limit=30):
    with _conn() as conn:
        rows = conn.execute("SELECT day, weight_kg FROM weights ORDER BY day DESC LIMIT ?", (limit,)).fetchall()
    return [{"day": r["day"], "weight_kg": r["weight_kg"]} for r in reversed(rows)]


def streak_days():
    """Consecutive days (ending today or yesterday) with at least one log of any kind."""
    with _conn() as conn:
        days = set()
        for table, col in (("meals", "ts"), ("workouts", "ts"), ("moods", "ts"), ("water", "ts")):
            days.update(r[0][:10] for r in conn.execute(f"SELECT {col} FROM {table}").fetchall())
        days.update(r[0] for r in conn.execute("SELECT day FROM sleep").fetchall())
        days.update(r[0] for r in conn.execute("SELECT day FROM weights").fetchall())
    streak = 0
    cursor = date.today()
    if cursor.isoformat() not in days:
        cursor -= timedelta(days=1)  # today isn't over yet; an unbroken streak may end yesterday
    while cursor.isoformat() in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def recent_entries(days=7):
    """Raw recent log lines, for the agent to reason over."""
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    out = {}
    with _conn() as conn:
        out["meals"] = [dict(r) for r in conn.execute(
            "SELECT ts, description, calories FROM meals WHERE ts >= ? ORDER BY ts", (cutoff,)).fetchall()]
        out["workouts"] = [dict(r) for r in conn.execute(
            "SELECT ts, activity, duration_min, intensity FROM workouts WHERE ts >= ? ORDER BY ts", (cutoff,)).fetchall()]
        out["moods"] = [dict(r) for r in conn.execute(
            "SELECT ts, rating, note FROM moods WHERE ts >= ? ORDER BY ts", (cutoff,)).fetchall()]
        out["sleep"] = [dict(r) for r in conn.execute(
            "SELECT day, hours, quality FROM sleep WHERE day >= ? ORDER BY day", (cutoff,)).fetchall()]
        out["weights"] = weight_history(days)
    return out
