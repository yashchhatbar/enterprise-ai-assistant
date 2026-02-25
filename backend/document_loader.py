
import os
import shutil
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.utils import setup_logger
from backend.config import Config

logger = setup_logger(__name__)

class DocumentLoader:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )

    def process_file(self, file_path: str, file_type: str) -> List[Document]:
        """Loads and splits a document based on its type."""
        try:
            logger.info(f"Processing file: {file_path}")
            
            if file_type == "application/pdf":
                loader = PyPDFLoader(file_path)
            elif file_type == "text/plain":
                loader = TextLoader(file_path)
            elif file_type == "text/csv":
                loader = CSVLoader(file_path)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Generated {len(chunks)} chunks from {file_path}")
            return chunks

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            raise e
        finally:
            # Clean up temp file if needed (handled by caller typically, but good practice to note)
            pass
