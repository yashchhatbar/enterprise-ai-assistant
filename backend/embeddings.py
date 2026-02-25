from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.utils import setup_logger

logger = setup_logger(__name__)

class EmbeddingManager:
    _embeddings = None

    @classmethod
    def get_embeddings(cls):
        if cls._embeddings is None:
            logger.info("⚡ Loading MiniLM model for the first time...")
            cls._embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"batch_size": 8}
            )
            logger.info("✅ MiniLM model loaded successfully.")
        return cls._embeddings
