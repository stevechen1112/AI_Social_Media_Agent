import os
from typing import List, Dict, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

class RAGService:
    def __init__(self):
        # Use Google Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # Use Local ChromaDB
        self.persist_directory = "./chroma_db"
        self.vector_store = Chroma(
            collection_name="brand_knowledge",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    async def add_documents(self, collection_name: str, texts: List[str], metadatas: List[Dict[str, Any]]):
        try:
            # Chroma handles collection creation automatically
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False

    async def query_similar(self, collection_name: str, query: str, limit: int = 3) -> List[str]:
        try:
            results = self.vector_store.similarity_search(query, k=limit)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error querying documents: {e}")
            return []

rag_service = RAGService()
