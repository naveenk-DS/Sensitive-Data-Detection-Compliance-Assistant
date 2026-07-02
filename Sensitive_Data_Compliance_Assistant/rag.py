import os
from typing import List, Any
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from langchain_ollama import OllamaEmbeddings
from config import VECTOR_DB_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL

def get_embeddings():
    """Get the Ollama embedding model."""
    # We use a standard embedding model like 'nomic-embed-text' or the default model.
    # Llama3 can also be used, but standard practice is nomic-embed-text or just the model.
    return OllamaEmbeddings(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )

def create_vector_store(text: str, document_id: str):
    """Chunk text, create embeddings, and store in FAISS."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    docs = [Document(page_content=chunk, metadata={"source": document_id}) for chunk in chunks]
    
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Save locally
    store_path = os.path.join(VECTOR_DB_DIR, document_id)
    vectorstore.save_local(store_path)
    return vectorstore

def load_vector_store(document_id: str):
    """Load existing FAISS store."""
    store_path = os.path.join(VECTOR_DB_DIR, document_id)
    if os.path.exists(store_path):
        embeddings = get_embeddings()
        return FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
    return None
