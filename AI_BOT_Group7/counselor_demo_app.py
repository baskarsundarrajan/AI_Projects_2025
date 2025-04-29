import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import os

# --- Load RAG Components ---

# Load sentence transformer model for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("counselor_faiss.index")

# Load responses for RAG
with open("counselor_responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

# --- Load Fine-Tuned Model ---

# Path to your fine-tuned model folder
model_path = "fine_tuned_flant5"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# --- RAG Search Function ---

def rag_search(query, k=1):
    query_embedding = embedder.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    top_responses = [responses[i] for i in I[0]]
    return top_responses

# --- Fine-Tuned Model Response Generation ---

def generate_finetuned_response(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).input_ids
    output = model.generate(
        input_ids,
        max_length=150,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
        no_repeat_ngram_size=3,
        num_return_sequences=1
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

# --- Main Chat Function ---

def chat():
    print("💬 Pandora the Counselor is ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() == "exit":
            print("👋 Pandora: Take care! See you soon.")
            break

        # Step 1: RAG Search
        rag_context = rag_search(user_input, k=1)[0]

        # Step 2: Build Combined Prompt
        final_prompt = (
            f"The student says: \"{user_input}\"\n\n"
            f"Advice you should consider: \"{rag_context}\"\n\n"
            f"Write a warm, supportive counselor response:"
        )

        # Step 3: Generate Final Response
        reply = generate_finetuned_response(final_prompt)
        print(f"\n🤖 Pandora: {reply}\n")

# --- Run the Chatbot ---

if __name__ == "__main__":
    chat()
