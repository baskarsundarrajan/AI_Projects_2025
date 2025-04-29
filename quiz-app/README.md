# Quiz App

A full-stack quiz application designed to test users' knowledge through interactive quizzes. Built with a modern tech stack comprising FastAPI, Celery, Redis, and Next.js, this application ensures efficient performance and scalability.

---
## 👨‍💻 Authors

- **Seamus .F. Rodrigues** (Roll No: 24P0620011)
- **Rohit M. Ghosarwadkar** (Roll No: 24P0620005)

---
## 🧰 Tech Stack

- **Backend:** FastAPI – A modern, fast (high-performance) web framework for building APIs with Python.
- **Task Queue:** Celery – An asynchronous task queue/job queue based on distributed message passing.
- **Message Broker:** Redis – An open-source, in-memory data structure store, used as a database, cache, and message broker.
- **Frontend:** Next.js – A React framework for building user interfaces with server-side rendering and static site generation.

---

## 📁 Project Structure

```
quiz-app/
├── backend/
│   └── app/
│       ├── main.py
│       ├── tasks.py
│       └── ...
├── frontend/
│   ├── pages/
│   ├── components/
│   └── ...
├── requirements.txt
├── test.py
├── .gitignore
└── .gitattributes
```

- `backend/app/`: Contains the FastAPI application and Celery task definitions.
- `frontend/`: Houses the Next.js frontend application.
- `requirements.txt`: Lists the Python dependencies required for the backend.
- `test.py`: A script for testing purposes.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.9+
- Node.js and npm
- Redis

---

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend/app
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: 
   venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r ../../requirements.txt
   ```

4. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

The API will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

### Celery Worker

1. Ensure Redis server is running.
2. Start the Celery worker:

   ```bash
   celery -A core.config.celery_config.celery worker --loglevel=info -Q file_processing
   ```

This will start the Celery worker to handle asynchronous tasks.

---

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install the required Node.js packages:

   ```bash
   npm install
   ```

3. Start the Next.js development server:

   ```bash
   npm run dev
   ```

The frontend will be accessible at [http://localhost:3000](http://localhost:3000).

---

> **Note:** Ensure that the backend server is running before executing the tests.

---

## 📌 Notes

- Ensure that the Redis server is running before starting the Celery worker.
- The frontend and backend servers should be running concurrently for the application to function correctly.
- Adjust the API endpoints in the frontend if the backend is hosted on a different URL or port.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome!  
Please fork the repository and submit a pull request for any enhancements or bug fixes.

