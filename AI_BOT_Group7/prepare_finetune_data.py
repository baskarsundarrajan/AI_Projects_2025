# prepare_finetune_data.py (with auto user-directed tone)

import json
import random

# Simple empathy-enhancing templates
RESPONSE_TEMPLATES = [
    "You're not alone — {response}",
    "{response} Remember, you're not facing this alone.",
    "{response} You're doing your best, and that's okay.",
    "{response} Let's get through this together.",
    "Hey, just so you know — {response}",
    "I hear you. {response}",
    "It’s valid to feel this way. {response}",
]

# Load intents.json
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fine_tune_data = []

# Convert each pattern-response into a training pair
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        for response in intent["responses"]:
            # Rewrite response with a user-focused template
            template = random.choice(RESPONSE_TEMPLATES)
            user_focused_response = template.format(response=response.strip())

            fine_tune_data.append({
                "instruction": pattern.strip(),
                "output": user_focused_response.strip()
            })

# Save to new fine-tuning dataset
with open("fine_tuning_dataset.json", "w", encoding="utf-8") as f:
    json.dump(fine_tune_data, f, indent=2)

print(f"✅ Created fine_tuning_dataset.json with {len(fine_tune_data)} friendly, user-focused Q&A pairs.")

