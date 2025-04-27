# Pandora: AI Counselor Bot 🤖💬
Michelle De Melo 24P0620007
Radhika Dabholkar 24P0620009
## 📚 Abstract
Pandora is an AI-driven virtual counselor designed to provide preliminary emotional support to students dealing with stress, loneliness, anxiety, and depression.
The system uses Retrieval-Augmented Generation (RAG) to offer empathetic, safe, and human-like conversations.

## 🚀 Technologies Used
- Python 3.10
- HuggingFace Transformers
- SentenceTransformers (MiniLM-L6-v2)
- FAISS (Facebook AI Similarity Search)
- Fine tuned model

## 🏛 System Architecture
User Input ➔ RAG Search ➔ Warm Response

## 📦 Folder Structure
Group7_PandoraCounselor/
├── report.pdf
├── slides.pptx
├── README.md
├── counselor_faiss_index/
├── fine_tuned_flant5/
├── src/
│   ├── counselor_demo_app_rag_only.py
│   ├── counselor_faiss.index
│   ├── counselor_responses.json
│   ├── intents_cleaned.json
|   ├── fine_tuning_dataset.json
│   ├── fine_tune_model.ipynb
│   ├── prepare_finetune_data.py
|   ├── build_faiss_index_hf.py
│   ├── counselor_demo_app.py
│   ├── prompt_engineering_hf.py
│   └── query_faiss_rag.py

## 🛠 How to Run
```bash
pip install faiss-cpu sentence-transformers
python src/counselor_demo_app_rag_only.py
```

💬 Sample Chat
User: I feel sad.
Pandora: It's okay to feel sad sometimes. You're not alone.

👩‍💻 Developed by: Michelle and Radhika
