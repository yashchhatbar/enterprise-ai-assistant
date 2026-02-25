
try:
    import langchain
    print(f"Langchain version: {langchain.__version__}")
except ImportError as e:
    print(f"Langchain import failed: {e}")

try:
    from langchain.chains import RetrievalQA
    print("RetrievalQA imported successfully from langchain.chains")
except ImportError as e:
    print(f"RetrievalQA import form langchain.chains failed: {e}")

try:
    from langchain.prompts import PromptTemplate
    print("PromptTemplate imported successfully from langchain.prompts")
except ImportError as e:
    print(f"PromptTemplate import from langchain.prompts failed: {e}")
