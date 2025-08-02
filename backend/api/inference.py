# backend/api/inference.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.inference import generate_response
import logging

router = APIRouter(prefix="/api/inference", tags=["Inference"])

class QueryRequest(BaseModel):
    user_id: int
    module_code: str
    prompt: str

@router.post("/")
def query_model(request: QueryRequest):
    try:
        response = generate_response(
            user_id=request.user_id,
            module_code=request.module_code,
            prompt=request.prompt
        )
        return {"response": response}
    except FileNotFoundError:
        logging.exception("Model files not found for user %s module %s", request.user_id, request.module_code)
        raise HTTPException(status_code=404, detail="Fine-tuned model not found for this user and module")
    except ValueError as ve:
        logging.exception("Validation error: %s", str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.exception("Unexpected error during inference")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
