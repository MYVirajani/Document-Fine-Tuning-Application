# backend/api/upload.py

from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import os
import shutil
from ..services.preprocessing import clean_and_save_document
from ..db.crud import get_user_by_id
from ..config import DATA_DIR

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_document(
    user_id: int = Form(...),
    moduleCode: str = Form(...),
    file: UploadFile = File(...)
):
    user_folder = Path(DATA_DIR) / f"user_{user_id}" / moduleCode
    latest_path = user_folder / "latest"
    latest_path.mkdir(parents=True, exist_ok=True)

    file_path = latest_path / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Clean and tokenize document
    clean_and_save_document(file_path)

    return JSONResponse(content={"message": "File uploaded and processed successfully."})
