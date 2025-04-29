import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Load RAG Components ---

# Load sentence transformer model for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("counselor_faiss.index")

# Load responses for RAG
with open("counselor_responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

# --- RAG Search Function ---

def rag_search(query, k=1):
    query_embedding = embedder.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    top_responses = [responses[i] for i in I[0]]
    return top_responses

# --- Main Chat Function ---

def chat():
    print("💬 Pandora the Counselor (RAG-Only Mode) is ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() == "exit":
            print("👋 Pandora: Take care! See you soon.")
            break

        # Step 1: RAG Search
        rag_context = rag_search(user_input, k=1)[0]

        # Step 2: Directly Use RAG Result
        print(f"\n🤖 Pandora: {rag_context}\n")

# --- Run the Chatbot ---

if __name__ == "__main__":
    chat()
