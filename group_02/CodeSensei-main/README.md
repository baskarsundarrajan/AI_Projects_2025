# 💡 CodeSensei

**CodeSensei** is an AI-powered coding assistant that helps you write, understand, and explore code using natural language. Whether you're debugging, learning a new language, or need help generating code, CodeSensei is your go-to companion.

---

## 🚀 Features

- 🔍 **Explain Mode** – Understand complex code in simple terms.
- ⚡ **Generate Mode** – Instantly generate code snippets or algorithms.
- 💬 **Ask Mode** – Ask questions about programming concepts or syntax.
- 🧠 **Auto Mode** – Context-aware suggestions as you type.
- 🌙 **Light/Dark Themes** – Easily toggle between day and night modes.
- 🧼 **Clean UI** – Minimal, focused interface for seamless productivity.

---

## 🛠️ Tech Stack

| Layer        | Tech                        |
|--------------|-----------------------------|
| Frontend     | React + Vite                |
| Styling      | Pure CSS                    |
| Backend      | FastAPI                     |
| AI Engine    | LLaMA 3.2                   |
| Deployment   | Localhost / Custom Hosting  |

---

## 🧑‍💻 Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.9+)
- `pip`, `virtualenv`, or `poetry`
- Access to LLaMA 3.2 model (locally or via API)

## 🔧 Frontend Setup (React + Vite)

```bash
# Clone the repo
git clone https://github.com/Shrooooyes/CodeSensei.git
cd CodeSensei
cd frontend
```

### Install frontend dependencies
```bash
npm install
```
### Start the frontend server
```bash
npm run dev
```

## 🧠 Backend Setup (FastAPI + LLaMA)

### Navigate to backend folder
```bash
cd backend/
```

### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run FastAPI server
```bash
uvicorn main:app --reload
```
---
## ⚠️ Make sure LLaMA 3.2 is accessible to your backend (e.g., via HuggingFace Transformers, Ollama, or API endpoint).
---

## 📁 Project Structure
```bash
CodeSensei/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   ├── public/
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   └── services/llm_handler.py
│
├── README.md
└── requirements.txt
```
---
## ✨ Screenshots
- Light Mode	
![image](https://github.com/user-attachments/assets/0b5783a9-bca7-4f20-84e4-74e30ca7df89)

- Dark Mode
![image](https://github.com/user-attachments/assets/fc240cf5-bad1-44b4-8383-8cef60482d57)

--- 

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

## 🙌 Acknowledgements
-  Meta’s LLaMA
-  FastAPI
-  Vite
-   React

---

## Crafted with 💙 for developers, by developers.
Let me know if you want it adjusted for deployment (like Vercel/Render), Dockerized, or integrated with GitHub Actions for CI/CD.

