import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from config import Config

class VectorStore:
    def __init__(self):
        """Initialize the vector store with free embeddings."""
        self.config = Config()
        self.persist_directory = self.config.CHROMA_PERSIST_DIRECTORY
        
        # Use free sentence-transformers embeddings
        embedding_config = self.config.get_embedding_config()
        
        if embedding_config["provider"] == "sentence-transformers":
            print(f"INFO: Using free embeddings: {embedding_config['model']}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embedding_config["model"],
                model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            # Fallback to OpenAI if configured
            try:
                from langchain_openai import OpenAIEmbeddings
                self.embeddings = OpenAIEmbeddings(
                    openai_api_key=self.config.OPENAI_API_KEY,
                    model="text-embedding-ada-002"
                )
                print("INFO: Using OpenAI embeddings")
            except ImportError:
                print("ERROR: OpenAI embeddings not available, falling back to sentence-transformers")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
        
        # Initialize ChromaDB
        try:
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="rag_documents"
            )
            print(f"SUCCESS: Vector store initialized at: {self.persist_directory}")
        except Exception as e:
            print(f"ERROR: Failed to initialize vector store: {e}")
            raise
    
    def add_documents(self, documents):
        """Add documents to the vector store."""
        try:
            if not documents:
                return False
            
            # Add documents to ChromaDB
            self.db.add_documents(documents)
            self.db.persist()
            
            print(f"SUCCESS: Added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to add documents: {e}")
            return False
    
    def similarity_search(self, query, k=None):
        """Perform similarity search."""
        try:
            if k is None:
                k = self.config.TOP_K_RESULTS
            
            results = self.db.similarity_search(query, k=k)
            print(f"INFO: Found {len(results)} relevant documents for query: '{query[:50]}...'")
            return results
            
        except Exception as e:
            print(f"ERROR: Search failed: {e}")
            return []
    
    def get_collection_stats(self):
        """Get statistics about the collection."""
        try:
            # Get basic stats
            collection = self.db._collection
            count = collection.count()
            
            return {
                "total_documents": count,
                "embedding_model": self.embeddings.model_name if hasattr(self.embeddings, 'model_name') else "unknown",
                "persist_directory": self.persist_directory,
                "status": "active"
            }
            
        except Exception as e:
            print(f"❌ Failed to get collection stats: {e}")
            return {
                "total_documents": 0,
                "embedding_model": "unknown",
                "persist_directory": self.persist_directory,
                "status": "error"
            }
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        try:
            # Delete the collection directory
            import shutil
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
                print("🗑️ Cleared vector store collection")
            
            # Reinitialize
            self.__init__()
            return True
            
        except Exception as e:
            print(f"❌ Failed to clear collection: {e}")
            return False
