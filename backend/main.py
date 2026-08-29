from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from auth import check_login
from rag import get_rag_response
from database import get_database_connection


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Models
# -------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    username: str
    question: str


# -------------------------
# Home API
# -------------------------

@app.get("/")
def home():

    return {
        "message": "RAG application backend is running"
    }


# -------------------------
# Login API
# -------------------------

@app.post("/login")
def login(request: LoginRequest):

    is_valid = check_login(
        request.username,
        request.password
    )

    if is_valid:

        return {
            "success": True,
            "message": "Login successful",
            "username": request.username
        }

    return {
        "success": False,
        "message": "Invalid username or password"
    }


# -------------------------
# Chat API
# -------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    print("1. Chat request received")
    print("2. Username:", request.username)
    print("3. Question:", request.question)

    # Test RAG
    try:
        answer = get_rag_response(request.question)
        print("4. RAG response:", answer)
    except Exception as e:
        print("ERROR in RAG:", e)
        return {
            "success": False,
            "message": f"RAG error: {str(e)}"
        }

    # Test MySQL
    try:
        print("5. Connecting to MySQL...")

        connection = get_database_connection()
        print("6. MySQL connected")

        cursor = connection.cursor()

        sql = """
            INSERT INTO query_logs (username, query_text)
            VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (request.username, request.question)
        )

        connection.commit()

        print("7. Query inserted successfully")

        cursor.close()
        connection.close()

    except Exception as e:
        print("ERROR in MySQL:", e)

        return {
            "success": False,
            "answer": answer,
            "message": f"MySQL error: {str(e)}"
        }

    print("8. Sending response to frontend")

    return {
        "success": True,
        "answer": answer
    }