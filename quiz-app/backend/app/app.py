from fastapi import FastAPI, Depends
from typing import Annotated
from core.vector_operations import VectorDBOperations as db
from services.generate_questions import generate_question
from services.evaluate import evaluate_batch
from fastapi.middleware.cors import CORSMiddleware
from api.v1.router import user, file_op

from pydantic import BaseModel


class UserAnswer(BaseModel):
    batch:list


app = FastAPI()

app.include_router(user.router)
app.include_router(file_op.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/gen-questions")
def gen_questions(user_id: Annotated[str, Depends(user.validate_token)]):
    client = db.connect_weaviate()
    res = generate_question(client, user_id)

    return {"questions": res}


@app.post("/evaluate-batch/")
def evaluate_batch_endpoint(batch:UserAnswer):
    """
    Endpoint to evaluate a batch of question-answer pairs.
    Expects a list of objects with question, answer, and optional user_answer.
    Returns evaluation results.
    """
    try:
        # Convert Pydantic model to list of dicts for evaluate_batch
        # data = [item.dict() for item in batch.data]
        # Call the evaluate_batch function
        # print(batch)
        results = evaluate_batch(batch.batch)
        return {"results": results}
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
