import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # AI Provider Selection
    AI_PROVIDER = os.getenv("AI_PROVIDER", "huggingface")  # ollama, openai, huggingface
    
    # OpenAI Configuration (if using OpenAI)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Ollama Configuration (FREE - runs locally)
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")  # phi3:mini, llama2, mistral, codellama, etc.
    
    # Hugging Face Configuration (FREE tier - FASTEST)
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-medium")
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 3))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    
    # Embedding Configuration
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "sentence-transformers")  # sentence-transformers, openai, ollama
    
    @classmethod
    def get_ai_config(cls):
        """Get configuration for the selected AI provider."""
        if cls.AI_PROVIDER == "ollama":
            return {
                "provider": "ollama",
                "base_url": cls.OLLAMA_BASE_URL,
                "model": cls.OLLAMA_MODEL,
                "is_free": True
            }
        elif cls.AI_PROVIDER == "huggingface":
            if not cls.HUGGINGFACE_API_KEY:
                raise ValueError("HUGGINGFACE_API_KEY is required when using Hugging Face provider")
            return {
                "provider": "huggingface",
                "api_key": cls.HUGGINGFACE_API_KEY,
                "model": cls.HUGGINGFACE_MODEL,
                "is_free": True
            }
        else:  # openai
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
            return {
                "provider": "openai",
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL,
                "is_free": False
            }
    
    @classmethod
    def get_embedding_config(cls):
        """Get configuration for embeddings."""
        if cls.EMBEDDING_PROVIDER == "sentence-transformers":
            return {
                "provider": "sentence-transformers",
                "model": "all-MiniLM-L6-v2",  # Fast, lightweight, free
                "is_free": True
            }
        elif cls.EMBEDDING_PROVIDER == "ollama":
            return {
                "provider": "ollama",
                "model": "nomic-embed-text",  # Free embedding model
                "is_free": True
            }
        else:  # openai
            return {
                "provider": "openai",
                "model": "text-embedding-ada-002",
                "is_free": False
            }
