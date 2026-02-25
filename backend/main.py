
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from backend.document_loader import DocumentLoader
from backend.embeddings import EmbeddingManager
from backend.vector_store import VectorStoreManager
from backend.rag_pipeline import RAGPipeline
from backend.config import Config
from backend.utils import setup_logger

# Initialize Logger
logger = setup_logger(__name__)

# Verify Environment
try:
    Config.validate()
except ValueError as e:
    logger.critical(f"Configuration Error: {e}")
    # In production, we might want to exit, but for dev we'll log

# Initialize Components
app = FastAPI(title="Enterprise AI Knowledge Assistant", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: Restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Instances (Lazy loading strategies can be applied for serverless)
embedding_function = EmbeddingManager.get_embeddings()
vector_store = VectorStoreManager(embedding_function)
rag_pipeline = RAGPipeline(vector_store)
document_loader = DocumentLoader()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Enterprise AI Assistant"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    ALLOWED_TYPES = [
        "application/pdf", 
        "text/plain", 
        "text/csv", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, TXT, CSV, and DOCX are allowed.")

    file_location = f"temp_{file.filename}"
    
    try:
        # Save file temporarily
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process Document
        chunks = document_loader.process_file(file_location, file.content_type)
        
        # Add metadata (source filename)
        for chunk in chunks:
            chunk.metadata["source"] = file.filename
            
        # Add to Vector Store
        vector_store.add_documents(chunks)
        
        return {"message": f"Successfully processed {file.filename}", "chunks": len(chunks)}

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/query", response_model=QueryResponse)
def query_knowledge_base(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    try:
        result = rag_pipeline.run_query(request.question)
        return result
    except Exception as e:
        import traceback
        print("\n🔥 GEMINI GENERATION ERROR 🔥\n")
        traceback.print_exc()
        return {"detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
