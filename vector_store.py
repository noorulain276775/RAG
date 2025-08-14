import os
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from config import Config

class VectorStore:
    """Manages vector storage and retrieval for the RAG system."""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=Config.OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize the vector store with ChromaDB."""
        try:
            # Check if vector store already exists
            if os.path.exists(Config.CHROMA_PERSIST_DIRECTORY):
                self.vector_store = Chroma(
                    persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
                print(f"Loaded existing vector store from {Config.CHROMA_PERSIST_DIRECTORY}")
            else:
                # Create new vector store
                self.vector_store = Chroma(
                    persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
                print(f"Created new vector store at {Config.CHROMA_PERSIST_DIRECTORY}")
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            # Fallback to in-memory store
            self.vector_store = Chroma(
                embedding_function=self.embeddings
            )
            print("Using in-memory vector store as fallback")
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector store."""
        try:
            if not documents:
                print("No documents to add")
                return False
            
            # Add documents to vector store
            self.vector_store.add_documents(documents)
            
            # Persist the changes
            self.vector_store.persist()
            
            print(f"Successfully added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """Perform similarity search for a query."""
        try:
            if k is None:
                k = Config.TOP_K_RESULTS
            
            results = self.vector_store.similarity_search(query, k=k)
            return results
            
        except Exception as e:
            print(f"Error performing similarity search: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """Perform similarity search with scores."""
        try:
            if k is None:
                k = Config.TOP_K_RESULTS
            
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
            
        except Exception as e:
            print(f"Error performing similarity search with score: {e}")
            return []
    
    def get_collection_stats(self) -> dict:
        """Get statistics about the vector store collection."""
        try:
            collection = self.vector_store._collection
            count = collection.count()
            
            stats = {
                "total_documents": count,
                "persist_directory": Config.CHROMA_PERSIST_DIRECTORY,
                "embedding_model": "text-embedding-ada-002"
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def clear_collection(self) -> bool:
        """Clear all documents from the vector store."""
        try:
            self.vector_store._collection.delete(where={})
            self.vector_store.persist()
            print("Vector store collection cleared")
            return True
            
        except Exception as e:
            print(f"Error clearing collection: {e}")
            return False
    
    def delete_documents(self, ids: List[str]) -> bool:
        """Delete specific documents by their IDs."""
        try:
            self.vector_store._collection.delete(ids=ids)
            self.vector_store.persist()
            print(f"Deleted {len(ids)} documents from vector store")
            return True
            
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False
