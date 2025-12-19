from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import shutil
import os
import tempfile
from app.services.document_processor import document_processor
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/upload-brand-info")
async def upload_brand_info(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "txt", "csv"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        texts = await document_processor.process_file(tmp_path, file_ext)
        # Use a generic collection name for now, or user-specific one
        collection_name = "brand_knowledge"
        await rag_service.add_documents(
            collection_name=collection_name,
            texts=texts,
            metadatas=[{"source": file.filename} for _ in texts]
        )
        return {"message": f"Successfully processed {len(texts)} chunks from {file.filename}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@router.get("/search-knowledge")
async def search_knowledge(query: str):
    results = await rag_service.query_similar("brand_knowledge", query)
    return {"results": results}
