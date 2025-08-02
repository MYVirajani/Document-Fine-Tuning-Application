# backend/api/upload.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil
from backend.services.preprocessing import clean_and_save_document
from backend.services.fine_tune import fine_tune_model

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("/")
async def upload_document(
    user_id: int = Form(...),
    module_code: str = Form(...),
    file: UploadFile = File(...)
):
    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".txt", ".pptx"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    upload_dir = Path(f"data/user_{user_id}/{module_code}/latest")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Clean and save cleaned version
    try:
        cleaned_file = clean_and_save_document(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleaning failed: {e}")

    # Trigger fine-tuning (can be async or queued in production)
    try:
        fine_tune_model(user_id, module_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fine-tuning failed: {e}")

    return {"message": "Document uploaded and fine-tuning started", "cleaned_file": str(cleaned_file)}
