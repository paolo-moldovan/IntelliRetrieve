from chromadb import Client, Settings
from chromadb.config import Settings
import numpy as np
from typing import List, Dict

class VectorDB:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, texts: List[str], metadata: List[Dict] = None):
        try:
            ids = [str(i) for i in range(len(texts))]
            
            self.collection.add(
                documents=texts,
                metadatas=metadata if metadata else [{}] * len(texts),
                ids=ids
            )
        except Exception as e:
            raise Exception(f"Error adding documents to vector database: {str(e)}")

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            documents = []
            for i in range(len(results['documents'][0])):
                documents.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            return documents
        except Exception as e:
            raise Exception(f"Error querying vector database: {str(e)}")

    def delete_collection(self):
        self.client.delete_collection("documents")
