# backend/routers/upload_router.py

import os
from fastapi import APIRouter, UploadFile, File
from backend.auth import get_current_user
from fastapi import Depends
from backend.services.pdf_services import extract_text
from backend.services.rag_service import split_text
from backend.services.embedding_service import store_chunks

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text(file_path)

    chunks = split_text(text)

    store_chunks(chunks, user.id)

    return {"filename": file.filename, "chunks_created": len(chunks)}
