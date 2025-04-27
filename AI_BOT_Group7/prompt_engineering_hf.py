# prompt_engineering_hf.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model and tokenizer
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# User input
user_input = "I feel like no one understands me and I’m overwhelmed with everything."

# Prompt formatted for flan-t5
prompt = f"You are an empathetic student counselor. A student says: '{user_input}'. What would you say?"

# Tokenize and generate response
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)

# Decode and print the response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Pandora:", response)
