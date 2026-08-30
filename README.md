# Simple RAG Application

A simple RAG-based web application built using **HTML, CSS, JavaScript, FastAPI, MySQL, FAISS, and OpenAI API**.

## Project Structure
```text
rag_project/
│
├── frontend/
│   ├── login.html
│   ├── chat.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── login.js
│       └── chat.js
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── rag.py
│   ├── llm.py
│   ├── document_loader.py
│   ├── create_faiss.py
│   ├── search_faiss.py
│  
│
├── documents/
│   ├── company.pdf
│   └── product.pdf
│
├── vector_db/
│   └── faiss_index/
│
├── .env
├── requirements.txt
├── .gitignore
└── README.md
'''

## Technologies

* Frontend: HTML, CSS, JavaScript
* Backend: FastAPI, Python
* Database: MySQL
* Vector Database: FAISS
* LLM: OpenAI API

## Application Flow

```text
User
 ↓
Login
 ↓
FastAPI
 ↓
MySQL
 ↓
Chat
 ↓
RAG
 ↓
FAISS
 ↓
OpenAI
 ↓
Answer
```

## Features

* User login
* Chat interface
* Document-based question answering
* FAISS vector search
* OpenAI response generation
* User query logging with timestamp

## Run the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### Frontend

From the project root:

```bash
python -m http.server 5500 --directory frontend
```

Frontend:

```text
http://127.0.0.1:5500/login.html
```

## Database

Create a MySQL database named:

```text
rag_app
```

Configure the MySQL connection in the backend.

## Environment Variables

Create `.env`:

```text
OPENAI_API_KEY=your_api_key

```

## Run open in two terminals for Frontend and backend 
1. python -m http.server 5500 --directory frontend
2. uvicorn main:app --reload

Run in Web browser " http://127.0.0.1:5500/login.html "



## Future Improvements

* Better authentication
* RAG evaluation
* Conversation history
* Docker deployment
* Production deployment
