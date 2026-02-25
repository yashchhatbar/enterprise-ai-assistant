
import langchain
import os

print(f"Langchain path: {langchain.__path__}")
try:
    print(f"Langchain dir: {os.listdir(langchain.__path__[0])}")
except Exception as e:
    print(e)

try:
    import langchain.chains
    print(f"Chains path: {langchain.chains.__path__}")
    print(f"Chains dir: {os.listdir(langchain.chains.__path__[0])}")
except ImportError as e:
    print(f"Import langchain.chains failed: {e}")
