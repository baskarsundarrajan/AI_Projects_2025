Grow To Glow 🌾 | AI_Projects_2025
Project Overview
Grow To Glow is an intelligent chatbot designed to assist farmers and nutrition enthusiasts in Goa. It provides seasonal advice, cultivation tips, and dietary suggestions based on local coastal and saline conditions. Powered by a combination of Retrieval-Augmented Generation (RAG) and Groq’s LLaMA 3.3 model, this system ensures accurate, timely, and expert recommendations.

The backend uses FastAPI, FAISS for vector search, and HuggingFace sentence-transformers for embeddings.

Installation Steps
Clone the repository:




git clone <your-repo-link>
cd grow-to-glow
Install the required dependencies:




pip install -r requirements.txt
Make sure you have a valid Groq API key and plant_qna.csv file in the project directory.

Run the application:




uvicorn rag_chatbot_groq:app --host 0.0.0.1 --port 8000 --reload
How to Run
Start the server with:




uvicorn rag_chatbot_groq:app --reload
Open your browser and go to:




http://localhost:8000/
Type your agricultural or dietary questions into the input box and get expert guidance.

Example
Question:
"What vegetables should I plant in Goa during May?"

Response:
"🌱 Hello there! Since it's May, it's a great time to start growing gourds like bottle gourd and bitter gourd. These crops thrive in Goa’s pre-monsoon climate. Happy farming! 🌾"

Team Members and Roles

Name	Roll No	Role
Anup Vivek Borker	24P0620002	Full Stack Development, RAG Setup
Tanavi Nipanicar	24P0620012	Dataset Curation, Prompt Engineering
Tanaya Chari	24P0620013	UI/UX Design, Frontend Integration
Class: M.Sc AI Part 1