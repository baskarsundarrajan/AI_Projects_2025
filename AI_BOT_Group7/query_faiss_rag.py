# query_faiss_rag.py

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("counselor_faiss.index")

# Load responses
with open("counselor_responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

# Function to query the index
def get_response(query, k=3):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    
    print("\n🎯 Top Matching Response(s):\n")
    for i in I[0]:
        print(f"🔹 {responses[i]}")
    return responses[I[0][0]]  # Return the best match

# Try a query!
if __name__ == "__main__":
    user_input = input("🗣️ You: ")
    response = get_response(user_input)
    print(f"\n🤖 Pandora: {response}")
