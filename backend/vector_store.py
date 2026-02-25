
import os
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from backend.config import Config
from backend.utils import setup_logger

logger = setup_logger(__name__)

class VectorStoreManager:
    def __init__(self, embedding_function):
        self.embedding_function = embedding_function
        self.index_path = Config.FAISS_INDEX_PATH
        self.db = self._load_or_create_index()

    def _load_or_create_index(self):
        """Loads FAISS index from disk or initializes a new state."""
        if os.path.exists(self.index_path):
            try:
                # Check for necessary files to confirm it's a valid index
                if os.path.exists(os.path.join(self.index_path, "index.faiss")):
                    logger.info(f"📂 Loading existing FAISS index from {self.index_path}...")
                    return FAISS.load_local(self.index_path, self.embedding_function, allow_dangerous_deserialization=True)
                else:
                    logger.warning(f"⚠️ Index path exists at {self.index_path} but no index file found.")
            except Exception as e:
                logger.error(f"❌ Failed to load FAISS index: {e}")
        
        logger.info("🆕 No existing index found. Initializing new vector store.")
        return None

    def add_documents(self, documents):
        """Adds documents to the vector store and saves to disk."""
        if not documents:
            return

        try:
            logger.info(f"📄 Adding {len(documents)} documents to vector store...")
            if self.db is None:
                # Create new vector store from documents
                self.db = FAISS.from_documents(documents, self.embedding_function)
                logger.info("✨ Created new FAISS index from documents.")
            else:
                self.db.add_documents(documents)
                logger.info("➕ Added documents to existing index.")
            
            self.save_index()
        except Exception as e:
            logger.error(f"❌ Error adding documents to vector store: {e}")
            raise e

    def save_index(self):
        """Saves current index to disk."""
        if self.db:
            try:
                # Ensure directory exists
                os.makedirs(self.index_path, exist_ok=True)
                self.db.save_local(self.index_path)
                logger.info(f"💾 FAISS index saved successfully to {self.index_path}")
            except Exception as e:
                logger.error(f"❌ Failed to save FAISS index: {e}")

    def get_retriever(self, k=4):
        """Returns a retriever object."""
        if self.db:
            return self.db.as_retriever(search_kwargs={"k": k})
        logger.warning("⚠️ Query attempted but no documents have been indexed yet.")
        return None
