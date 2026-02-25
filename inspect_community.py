
import langchain_community
import os

print(f"Langchain Community path: {langchain_community.__path__}")
try:
    print(f"Community dir: {os.listdir(langchain_community.__path__[0])}")
except Exception as e:
    print(e)

try:
    import langchain_community.chains
    print(f"Community chains path: {langchain_community.chains.__path__}")
    print(f"Community chains dir: {os.listdir(langchain_community.chains.__path__[0])}")
except ImportError as e:
    print(f"Import langchain_community.chains failed: {e}")
