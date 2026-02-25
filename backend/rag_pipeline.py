
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from backend.config import Config
from backend.utils import setup_logger

logger = setup_logger(__name__)

class RAGPipeline:
    def __init__(self, vector_store_manager):
        self.vector_store_manager = vector_store_manager
        self.llm = self._get_llm()
        self.prompt_template = self._create_prompt_template()

    def _get_llm(self):
        return ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL,
            temperature=0.3,
            convert_system_message_to_human=True
        )

    def _create_prompt_template(self):
        template = """
You are a helpful enterprise AI assistant.

Answer ONLY from the provided context.

If the answer is not in the context, say:
"Information not available in company documents."

Context:
{context}

Question:
{question}

Answer:
"""
        return PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )

    def run_query(self, query):
        retriever = self.vector_store_manager.get_retriever()
        if not retriever:
            return {"answer": "No documents uploaded yet. Please upload documents first.", "sources": []}

        # Create RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

        try:
            logger.info(f"Processing query: {query}")
            result = qa_chain.invoke({"query": query})
            
            answer = result.get("result", "")
            source_docs = result.get("source_documents", [])
            
            # Format sources
            sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]
            # Deduplicate sources
            sources = list(set(sources))

            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return {"answer": "An error occurred while processing your request.", "sources": []}
