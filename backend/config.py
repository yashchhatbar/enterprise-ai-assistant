
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Support both key names, prioritizing GEMINI_API_KEY as requested
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_API_KEY = GEMINI_API_KEY or os.getenv("GOOGLE_API_KEY")
    
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
    MAX_EMBEDDING_BATCH = int(os.getenv("MAX_EMBEDDING_BATCH", 32))
    EMBEDDING_MODEL = "models/text-embedding-004"
    LLM_MODEL = "gemini-1.5-flash"

    @staticmethod
    def validate():
        if not Config.GOOGLE_API_KEY:
            raise ValueError("❌ No API key found. Please set GEMINI_API_KEY in your environment.")
