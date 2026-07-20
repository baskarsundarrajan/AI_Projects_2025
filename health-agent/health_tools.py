"""Tool definitions (Ollama tool-calling schema) and their implementations.

Each tool the model calls maps to a database operation. execute_tool()
returns a plain dict that gets fed back to the model as the tool result.
"""

import database as db

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "log_meal",
            "description": "Record a meal or snack the user ate. Estimate calories yourself if the user doesn't give them.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "What was eaten, e.g. '2 rotis with dal and salad'"},
                    "calories": {"type": "integer", "description": "Estimated total calories"},
                },
                "required": ["description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_workout",
            "description": "Record physical activity or exercise the user did.",
            "parameters": {
                "type": "object",
                "properties": {
                    "activity": {"type": "string", "description": "e.g. 'walking', 'yoga', 'gym - upper body'"},
                    "duration_min": {"type": "integer", "description": "Duration in minutes"},
                    "intensity": {"type": "string", "enum": ["light", "moderate", "intense"]},
                },
                "required": ["activity", "duration_min"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_mood",
            "description": "Record the user's current mood or emotional state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rating": {"type": "integer", "description": "1 (very low) to 5 (great)"},
                    "note": {"type": "string", "description": "Short note on why, in the user's words"},
                },
                "required": ["rating"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_water",
            "description": "Record glasses of water the user drank.",
            "parameters": {
                "type": "object",
                "properties": {
                    "glasses": {"type": "integer", "description": "Number of glasses, default 1"},
                },
                "required": ["glasses"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_sleep",
            "description": "Record how long the user slept last night.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hours": {"type": "number", "description": "Hours slept"},
                    "quality": {"type": "string", "enum": ["poor", "ok", "good"]},
                },
                "required": ["hours"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_weight",
            "description": "Record the user's body weight measurement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {"type": "number", "description": "Weight in kilograms"},
                },
                "required": ["weight_kg"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_profile",
            "description": "Save a fact about the user for future reference: name, age, sex, height_cm, goal, conditions, diet_preference, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "e.g. 'goal', 'age', 'diet_preference'"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_history",
            "description": "Fetch the user's logged data for the last N days (meals, workouts, moods, sleep, weight, daily totals). Call this before answering questions about trends, progress, or 'how am I doing'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "How many days back to fetch, default 7"},
                },
                "required": [],
            },
        },
    },
]


def execute_tool(name, args):
    args = args or {}
    try:
        if name == "log_meal":
            db.log_meal(args["description"], args.get("calories"))
            return {"status": "logged", "meal": args["description"]}
        if name == "log_workout":
            db.log_workout(args["activity"], args["duration_min"], args.get("intensity"))
            return {"status": "logged", "workout": args["activity"]}
        if name == "log_mood":
            db.log_mood(args["rating"], args.get("note"))
            return {"status": "logged", "mood": args["rating"]}
        if name == "log_water":
            db.log_water(args.get("glasses", 1))
            return {"status": "logged", "water_today": db.day_totals()["water_glasses"]}
        if name == "log_sleep":
            db.log_sleep(args["hours"], args.get("quality"))
            return {"status": "logged", "sleep_hours": args["hours"]}
        if name == "log_weight":
            db.log_weight(args["weight_kg"])
            return {"status": "logged", "weight_kg": args["weight_kg"]}
        if name == "update_profile":
            db.set_profile(args["key"], args["value"])
            return {"status": "saved", "profile": db.get_profile()}
        if name == "get_history":
            days = int(args.get("days", 7) or 7)
            return {
                "daily_totals": db.last_n_days(min(days, 30)),
                "entries": db.recent_entries(min(days, 30)),
                "streak_days": db.streak_days(),
            }
        return {"error": f"unknown tool: {name}"}
    except (KeyError, TypeError, ValueError) as e:
        return {"error": f"bad arguments for {name}: {e}"}
