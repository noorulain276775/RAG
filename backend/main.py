from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import tempfile
import shutil
from pathlib import Path

# Import RAG system components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from document_loader import DocumentLoader
from vector_store import VectorStore
from rag_system import RAGSystem

app = FastAPI(title="RAG System API", version="1.0.0")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG components
rag_system = None
document_loader = None
vector_store = None

class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 3

class DocumentResponse(BaseModel):
    id: str
    name: str
    size: int
    type: str
    status: str
    chunks: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    num_sources: int

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system components on startup."""
    global rag_system, document_loader, vector_store
    
    try:
        print("🚀 Initializing RAG System...")
        
        # Initialize components
        document_loader = DocumentLoader()
        vector_store = VectorStore()
        rag_system = RAGSystem()
        
        # Connect components
        rag_system.set_components(vector_store, document_loader)
        
        print("✅ RAG System initialized successfully!")
        print(f"🤖 Using AI provider: {rag_system.ai_config['provider']}")
        print(f"💰 Free to use: {rag_system.ai_config['is_free']}")
        
    except Exception as e:
        print(f"❌ Failed to initialize RAG System: {e}")
        print("💡 Make sure Ollama is running or check your configuration")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "RAG System API",
        "status": "running",
        "rag_system_ready": rag_system is not None,
        "ai_provider": rag_system.ai_config['provider'] if rag_system else "unknown",
        "is_free": rag_system.ai_config['is_free'] if rag_system else False
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check."""
    if not rag_system:
        return {
            "status": "unhealthy",
            "rag_system": False,
            "document_loader": False,
            "vector_store": False,
            "error": "RAG system not initialized"
        }
    
    return {
        "status": "healthy",
        "rag_system": True,
        "document_loader": True,
        "vector_store": True,
        "ai_provider": rag_system.ai_config['provider'],
        "ai_model": rag_system.ai_config['model'],
        "is_free": rag_system.ai_config['is_free'],
        "embedding_provider": rag_system.config.get_embedding_config()['provider']
    }

@app.post("/api/upload", response_model=List[DocumentResponse])
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process documents."""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    uploaded_docs = []
    
    for file in files:
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
                # Write uploaded content to temp file
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                # Process document with RAG system
                documents = document_loader.load_file(tmp_file_path)
                
                if documents:
                    # Add to vector store
                    success = vector_store.add_documents(documents)
                    
                    if success:
                        doc_response = DocumentResponse(
                            id=str(len(uploaded_docs) + 1),
                            name=file.filename,
                            size=len(content),
                            type=file.content_type or "unknown",
                            status="processed",
                            chunks=len(documents)
                        )
                        uploaded_docs.append(doc_response)
                    else:
                        raise HTTPException(status_code=500, detail=f"Failed to add {file.filename} to vector store")
                else:
                    raise HTTPException(status_code=400, detail=f"No content extracted from {file.filename}")
                    
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
    
    return uploaded_docs

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_rag(request: QueryRequest):
    """Chat with the RAG system."""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    try:
        # Get RAG response
        response = rag_system.query(request.question, k=request.k)
        
        if response.get('error'):
            raise HTTPException(status_code=500, detail=response['error'])
        
        return ChatResponse(
            answer=response['answer'],
            sources=response['sources'],
            num_sources=response['num_sources']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents."""
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    
    try:
        stats = vector_store.get_collection_stats()
        return {
            "total_documents": stats.get('total_documents', 0),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting document stats: {str(e)}")

@app.delete("/api/documents")
async def clear_documents():
    """Clear all documents from the vector store."""
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    
    try:
        success = vector_store.clear_collection()
        if success:
            return {"message": "All documents cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear documents")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")

@app.post("/api/sample-documents")
async def load_sample_documents():
    """Load sample documents for testing."""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    try:
        # Create sample documents
        sample_docs = document_loader.create_sample_documents()
        
        if sample_docs:
            # Add to vector store
            success = vector_store.add_documents(sample_docs)
            
            if success:
                return {
                    "message": f"Loaded {len(sample_docs)} sample documents successfully",
                    "count": len(sample_docs)
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to add sample documents to vector store")
        else:
            raise HTTPException(status_code=500, detail="Failed to create sample documents")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sample documents: {str(e)}")

@app.get("/api/system-info")
async def get_system_info():
    """Get system configuration and statistics."""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    try:
        system_info = rag_system.get_system_info()
        return system_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting system info: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
