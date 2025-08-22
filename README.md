# RAG System - AI-Powered Document Q&A

A comprehensive Retrieval-Augmented Generation (RAG) system with a modern Next.js frontend and Python backend. Upload documents and ask questions with AI-powered context awareness.

## Features

- Document Upload: Support for PDF, TXT, DOC, Markdown, and code files
- AI-Powered Q&A: Ask questions about your documents with full context
- Smart Retrieval: Vector-based similarity search for relevant content
- Interactive Chat: Modern chat interface with source citations
- Responsive Design: Beautiful Next.js frontend with Tailwind CSS
- Fast API: FastAPI backend with real-time document processing
- Multiple AI Providers: Support for Ollama (FREE), OpenAI, and Hugging Face
- Free Embeddings: Local sentence-transformers for cost-free vector generation

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI       │    │   RAG System    │
│   Frontend      │◄──►│   Backend       │◄──►│   (Python)      │
│   (Port 3000)   │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Project Structure

```
RAG/
├── frontend/                 # Next.js Frontend
│   ├── app/                 # App Router
│   ├── components/          # React Components
│   ├── package.json         # Frontend Dependencies
│   └── tailwind.config.js   # Tailwind Configuration
├── backend/                  # FastAPI Backend
│   ├── main.py              # FastAPI Application
│   ├── run.py               # Backend Runner
│   └── requirements.txt     # Backend Dependencies
├── vector_store.py          # Vector Database
├── rag_system.py            # Core RAG Logic
├── config.py                # Configuration
├── requirements.txt          # Python Dependencies
└── README.md                # This File
```

## Quick Start

### Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- Git (optional)

### 1. Initial Setup

```bash
# Clone or navigate to project directory
cd RAG

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Install Ollama (FREE AI - Recommended)

1. Go to https://ollama.ai/download
2. Download installer for your operating system
3. Install and restart your computer
4. Open terminal and run:
   ```bash
   ollama serve
   ollama pull phi3:mini
   ```

### 3. Start the System

You need 2 terminal windows:

**Terminal 1 (Backend):**
```bash
cd backend
python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### 4. Access Your System

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## How It Works

### Document Processing Pipeline

1. **Upload**: Drag & drop or select files through the web interface
2. **Chunking**: Documents are split into smaller, manageable pieces (1000 characters by default)
3. **Embedding**: Text chunks are converted to numerical vectors using sentence-transformers (FREE)
4. **Storage**: Vectors are stored in ChromaDB for fast retrieval
5. **Retrieval**: When you ask a question, relevant chunks are found using similarity search
6. **Generation**: AI generates contextual answers using the retrieved information
7. **Response**: You receive the answer with source citations

### Step-by-Step Example

**Scenario**: User wants to know about AI from a research paper

1. **Document Upload**: User uploads AI_Research_Paper.pdf
2. **Processing**: System chunks the document and creates embeddings
3. **Question**: User asks "What are the main benefits of AI?"
4. **Retrieval**: System finds the most relevant chunks about AI benefits
5. **Generation**: AI generates answer using retrieved context
6. **Display**: User sees answer + source citations

## Technical Components

### Frontend (Next.js)

- **Document Upload**: Drag & drop interface with file preview
- **Chat Interface**: Real-time Q&A with message history
- **Document Management**: File organization and status tracking
- **Settings Panel**: Configuration and system information
- **Responsive Design**: Works on desktop and mobile devices

### Backend (FastAPI)

- **API Endpoints**: RESTful interface for all operations
- **Document Processing**: Multi-format file handling
- **RAG Integration**: Connects all system components
- **Error Handling**: Robust error management and logging
- **CORS Support**: Enables frontend-backend communication

### RAG System (Python)

- **Document Loader**: Processes PDF, TXT, DOC, Markdown, and code files
- **Vector Store**: ChromaDB for efficient similarity search
- **AI Provider**: Ollama (FREE), Hugging Face, or OpenAI integration
- **Prompt Engineering**: Optimized prompts for RAG applications
- **Text Chunking**: Intelligent document splitting with overlap

## Configuration

### Environment Variables (.env)

```env
# AI Provider Selection
AI_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini

# Embedding Configuration (FREE)
EMBEDDING_PROVIDER=sentence-transformers

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=3
TEMPERATURE=0.7
```

### Available AI Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| phi3:mini | 3.8B | Very Fast | Good | Quick responses |
| llama2 | 7B | Fast | High | General RAG |
| mistral | 7B | Very Fast | High | Quick responses |
| codellama | 7B | Fast | Very High | Technical docs |

## API Endpoints

### Health & System
- `GET /api/health` - System health check
- `GET /api/system-info` - System configuration and status

### Document Management
- `POST /api/upload` - Upload documents
- `GET /api/documents` - List all documents
- `DELETE /api/documents` - Clear all documents

### Chat & Q&A
- `POST /api/chat` - Ask questions and get AI responses

## Testing the System

### 1. Ask Questions

```bash
# Via API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'

# Via Frontend
# Go to Chat tab → Type your question
```

### 2. Check System Health

```bash
# Health check
curl http://localhost:8000/api/health

# System info
curl http://localhost:8000/api/system-info
```

## Monitoring & Debugging

### Backend Logs

Watch the backend terminal for:
- System initialization messages
- Document processing status
- AI model responses
- Error messages and stack traces

### Frontend Console

Open browser DevTools to see:
- API requests and responses
- Frontend errors and warnings
- Performance metrics
- Network activity

### API Documentation

Visit http://localhost:8000/docs for:
- Interactive API testing
- Endpoint documentation
- Request/response examples
- Schema definitions

## Common Issues & Solutions

### 1. "Ollama not found"

```bash
# Install Ollama from https://ollama.ai/download
# Restart computer after installation
# Then run:
ollama serve
ollama pull phi3:mini
```

### 2. "Port already in use"

```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill the process or use different ports
```

### 3. "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt
cd frontend && npm install
```

### 4. "Slow responses"

- Use smaller AI models (phi3:mini instead of llama2)
- Check if GPU acceleration is available
- Ensure sufficient RAM (8GB+ recommended)
- Use local embeddings instead of API calls

## Performance Optimization

### GPU Acceleration

For NVIDIA GPUs:
```bash
# Install CUDA toolkit
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Memory Optimization

- Use smaller models for faster responses
- Adjust chunk sizes based on available memory
- Enable model quantization for Ollama models
- Monitor memory usage during operation

### Storage Considerations

- Vector embeddings are stored locally in ChromaDB
- AI models are downloaded once and cached
- Document chunks are stored as text for quick access
- Regular cleanup of unused documents recommended

## Security Features

- Local processing for sensitive documents
- No data sent to external APIs (with Ollama)
- Environment-based configuration
- Input validation and sanitization
- CORS configuration for frontend access

## File Format Support

### Supported Formats

- **PDF**: Full text extraction with PyPDF
- **Text**: Plain text and markdown files
- **Code**: Python, JavaScript, HTML, CSS, and more
- **Documents**: Microsoft Office formats (if dependencies installed)

### Processing Capabilities

- Automatic format detection
- Text extraction and cleaning
- Metadata preservation
- Error handling for corrupted files
- Progress tracking for large files

## Development

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/RAG.git
cd RAG

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# Start development servers
# Terminal 1: cd backend && python run.py
# Terminal 2: cd frontend && npm run dev
```

### Code Structure

- **Modular Design**: Separate concerns for different components
- **Configuration Management**: Centralized settings with environment overrides
- **Error Handling**: Comprehensive error catching and logging
- **Testing**: Unit tests for core functionality
- **Documentation**: Inline code documentation and examples

### Extending the System

- Add new document formats in `backend/document_loader.py`
- Implement new AI providers in `rag_system.py`
- Create custom embedding models in `vector_store.py`
- Add new API endpoints in `backend/main.py`
- Extend frontend components in `frontend/components/`

## System Requirements

### Minimum Requirements

- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for models and data
- **OS**: Windows 10+, macOS 10.15+, or Linux

### Recommended Requirements

- **CPU**: Intel i7/AMD Ryzen 7 or better
- **RAM**: 16GB or more
- **Storage**: 50GB+ free space for multiple models
- **GPU**: NVIDIA GPU with CUDA support (optional)
- **OS**: Latest stable version

### Network Requirements

- Internet connection for initial setup and model downloads
- Local network access for frontend-backend communication
- Optional: Stable connection for Hugging Face Hub models

## Troubleshooting Guide

### Startup Issues

1. **Check Python version**: Ensure Python 3.8+ is installed
2. **Verify dependencies**: Run `pip list` to check installed packages
3. **Check ports**: Ensure ports 3000 and 8000 are available
4. **Environment variables**: Verify .env file configuration

### Runtime Issues

1. **Memory errors**: Reduce chunk sizes or use smaller models
2. **Slow performance**: Check GPU availability and model sizes
3. **Connection errors**: Verify Ollama service is running
4. **File upload issues**: Check file permissions and formats

### AI Model Issues

1. **Model not found**: Download required models with `ollama pull`
2. **Poor responses**: Adjust temperature and other parameters
3. **Slow generation**: Use smaller models or enable GPU acceleration
4. **Context errors**: Check document chunking and retrieval settings

## Success Indicators

### When Everything Works

1. Backend shows "RAG System initialized successfully"
2. Frontend loads without errors
3. Document upload completes successfully
4. AI responds to questions with context
5. Sources are properly cited
6. Vector database shows document statistics

### Performance Metrics

- Document upload: Less than 30 seconds for typical files
- Question response: Less than 10 seconds
- Similarity search: Less than 2 seconds
- Memory usage: Stable during operation
- CPU usage: Reasonable for model size

## Next Steps After Setup

1. **Upload Your Documents**: Start with small files for testing
2. **Ask Questions**: Begin with simple questions and test follow-ups
3. **Customize Settings**: Adjust chunk sizes, models, and parameters
4. **Scale Up**: Add more documents and experiment with different models
5. **Integrate**: Connect with existing document management systems
6. **Deploy**: Move to production environment with proper security

## Advanced Features

### Custom Models

```bash
# Create custom Ollama model
ollama create mymodel -f Modelfile

# Modelfile example:
FROM phi3:mini
PARAMETER temperature 0.7
PARAMETER top_p 0.9
```

### Batch Processing

- Upload multiple documents simultaneously
- Process large document collections
- Background processing for long operations
- Progress tracking and status updates

### Export & Backup

- Export processed documents and embeddings
- Backup vector database and configurations
- Migrate between different environments
- Version control for document collections

This RAG system provides a powerful, scalable solution for document-based question answering with AI. The modular architecture allows for easy customization and extension while maintaining high performance and reliability.
