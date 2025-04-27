import os
from datasets import load_dataset
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq
from langchain.docstore.document import Document
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn

# Configuration
os.environ["GROQ_API_KEY"] = "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"

# Load dataset and create vector store
dataset = load_dataset("csv", data_files="plant_qna.csv")
docs = dataset["train"]

embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_chunks = [Document(page_content=row["question"] + "\n" + row["answer"]) for row in docs]
vectordb = FAISS.from_documents(text_chunks, embedding=embedder)
vectordb.save_local("vector_store/")

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# FastAPI setup
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title> Grow To Glow Bot</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to bottom right, #d4f1c5, #f9fbe7);
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                border-radius: 16px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                padding: 30px;
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #2e7d32;
                text-align: center;
            }
            textarea {
                width: 100%;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #ccc;
                resize: vertical;
                font-size: 1rem;
            }
            button {
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #66bb6a;
                color: white;
                font-size: 1rem;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #388e3c;
            }
            .response-box {
                margin-top: 30px;
                background: #f1f8e9;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #c5e1a5;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾  Grow To Glow 🌴</h1>
            <textarea id="query" rows="5" placeholder="Ask your question here..."></textarea>
            <button id="ask-button">Ask the Expert</button>
            <div class="response-box" id="response">Your answer will appear here!</div>
        </div>

        <script>
            document.getElementById("ask-button").onclick = async function () {
                const query = document.getElementById("query").value.trim();
                const responseElement = document.getElementById("response");
                if (!query) {
                    alert("Please enter a question!");
                    return;
                }

                responseElement.innerText = "Thinking... 🌱";

                try {
                    const res = await fetch("/ask", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ query })
                    });

                    const data = await res.json();
                    responseElement.innerText = data.response || "No response from bot.";
                } catch (error) {
                    console.error("Error:", error);
                    responseElement.innerText = "Error contacting the bot.";
                }
            };
        </script>
    </body>
    </html>
    """



@app.post("/ask")
async def ask_question(req: QueryRequest):
    results = vectordb.similarity_search(req.query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    current_month = datetime.now().strftime("%B")

    system_prompt = f"""
    You are an expert agronomist and nutritionist specializing in coastal saline agriculture in Goa.
    Today is {current_month}. Greet the user warmly and suggest what crops or fruits are best to grow or consume this month in Goa's climate.
    Provide helpful, friendly, and varied responses that include seasonal advice, cultivation tips, and nutritional suggestions.
    Use a conversational tone.
    
    Use the following context to answer the user's question:
    {context}
    """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.query}
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=0.9
    )

    return {"response": response.choices[0].message.content}
if __name__ == "__main__":
    uvicorn.run("rag_chatbot_groq:app", host="0.0.0.1", port=8000, reload=True)
