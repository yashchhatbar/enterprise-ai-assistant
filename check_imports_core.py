
try:
    from langchain_core.prompts import PromptTemplate
    print("PromptTemplate imported successfully from langchain_core.prompts")
except ImportError as e:
    print(f"PromptTemplate import from langchain_core.prompts failed: {e}")

try:
    from langchain.chains import RetrievalQA
    print("RetrievalQA imported successfully from langchain.chains")
except ImportError:
    print("Could not import RetrievalQA from langchain.chains")
    try:
        from langchain.chains import create_retrieval_chain
        print("create_retrieval_chain imported successfully from langchain.chains")
    except ImportError:
        print("Could not import create_retrieval_chain from langchain.chains")
