"""
@Author: Srini Yedluri
@Date: 3/21/26
@File: main_test.py
"""

import os
import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from pathlib import Path

def load_data(file_name):
    """Load sample knowledge base content from JSON file."""
    src_dir = Path(__file__).parent.parent.parent
    dataset_file = os.path.join(src_dir, "data", file_name)
    with open(dataset_file, 'r') as file:
        return json.load(file)

def chunk_text(text, chunk_size=100):
    """Chunk text into smaller pieces for better processing."""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def chunk_dataset(data, chunk_size=100):
    all_chunks = []
    for doc_id, doc in enumerate(data):
        doc_text = doc["content"]
        doc_chunks = chunk_text(doc_text, chunk_size)
        for chunk_id, chunk_str in enumerate(doc_chunks):
            all_chunks.append({
                "id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk_str,
            })
    return all_chunks

def build_chroma_collection(chunks, collection_name="rag_collection"):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    client = Client(Settings())
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embed_func)

    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{c['id']}_{c['chunk_id']}" for c in chunks]
    metadatas = [{"id": c["id"], "chunk_id": c["chunk_id"]} for c in chunks]

    # Add documents to the collection
    collection.add(documents=texts, metadatas=metadatas, ids=ids)

    return collection

def load_collection(collection_name="rag_collection"):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    client = Client(Settings())
    return client.get_or_create_collection(name=collection_name, embedding_function=embed_func)

def build_rag():
    data = load_data("todos.json")
    chunked_data = chunk_dataset(data)
    build_chroma_collection(chunked_data)