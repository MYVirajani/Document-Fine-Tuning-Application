# backend/api/inference.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.inference import run_inference

router = APIRouter(prefix="/inference", tags=["Inference"])

class InferenceRequest(BaseModel):
    user_id: int
    moduleCode: str
    prompt: str

@router.post("/")
def query_model(request: InferenceRequest):
    response = run_inference(user_id=request.user_id, moduleCode=request.moduleCode, prompt=request.prompt)
    if response is None:
        raise HTTPException(status_code=404, detail="Model or data not found")
    return {"response": response}
