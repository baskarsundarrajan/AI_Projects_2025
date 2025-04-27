# build_faiss_index_hf.py

import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# Load your intents.json
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten intents into a list of (text, response) pairs
documents = []
responses = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        for response in intent["responses"]:
            doc = f"User: {pattern}\nBot: {response}"
            documents.append(doc)
            responses.append(response)

# Load sentence transformer model (free, local)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(documents, convert_to_numpy=True)

# Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Save index + metadata
faiss.write_index(index, "counselor_faiss.index")

# Save response mapping
with open("counselor_responses.json", "w", encoding="utf-8") as f:
    json.dump(responses, f, indent=2)

print("✅ FAISS index and responses saved successfully!")
