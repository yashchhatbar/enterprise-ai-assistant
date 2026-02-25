
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import inspect

print(GoogleGenerativeAIEmbeddings.__init__.__annotations__)

emb = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key="AIzaSyAc0OSUAo74zndQvzyJOW-xf-pwHdo54XU")
print(dir(emb))
try:
    print(f"Task type: {emb.task_type}")
except:
    pass
