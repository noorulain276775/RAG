#!/usr/bin/env python3
"""
RAG System Backend Runner
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting RAG System Backend...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 API Documentation at: http://localhost:8000/docs")
    print("🔧 Health Check at: http://localhost:8000/api/health")
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
