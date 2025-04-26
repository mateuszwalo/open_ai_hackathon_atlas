from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from typing import List, Dict, Any

def load_faiss_index(index_path: str, embedding_model: str = "text-embedding-3-small"):
    """Wczytuje zapisany indeks FAISS"""
    embeddings = OpenAIEmbeddings(model=embedding_model)
    return FAISS.load_local(
        folder_path=index_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # Wymagane dla nowszych wersji LangChain
    )

# Przykład użycia:
vectorstore = load_faiss_index("vector")