from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Day 35 FastAPI Basics",
    version="1.0.0",
)


# -----------------------------------
# Request model
# -----------------------------------

class LearningRequest(
    BaseModel
):

    topic: str
    level: str = "beginner"


# -----------------------------------
# Root endpoint
# -----------------------------------

@app.get("/")
async def root():

    return {
        "message":
            "Day 35 FastAPI API is running"
    }


# -----------------------------------
# Health endpoint
# -----------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }


# -----------------------------------
# Path parameter
# -----------------------------------

@app.get(
    "/hello/{name}"
)
async def hello(
    name: str,
):

    return {
        "message":
            f"Hello {name}"
    }


# -----------------------------------
# Typed path parameter
# -----------------------------------

@app.get(
    "/square/{number}"
)
async def square(
    number: int,
):

    return {
        "number": number,
        "square": number * number,
    }


# -----------------------------------
# Query parameter
# -----------------------------------

@app.get(
    "/topics"
)
async def topics(
    limit: int = 3,
):

    all_topics = [
        "RAG",
        "LangChain",
        "LangGraph",
        "MCP",
        "Agents",
    ]

    return {
        "topics":
            all_topics[:limit]
    }


# -----------------------------------
# Request body
# -----------------------------------

@app.post(
    "/learn"
)
async def learn(
    request: LearningRequest,
):

    return {
        "topic":
            request.topic,

        "level":
            request.level,

        "message":
            (
                f"Start learning "
                f"{request.topic} "
                f"at {request.level} level."
            ),
    }