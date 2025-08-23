# RAG System - AI-Powered Document Q&A

A comprehensive Retrieval-Augmented Generation (RAG) system with a modern Next.js frontend and Python backend. Upload documents and ask questions with AI-powered context awareness.

## Features

- **Document Upload**: Support for PDF, TXT, DOC, Markdown, and code files
- **AI-Powered Q&A**: Ask questions about your documents with full context
- **Smart Retrieval**: Vector-based similarity search for relevant content
- **Interactive Chat**: Modern chat interface with source citations
- **Responsive Design**: Beautiful Next.js frontend with Tailwind CSS
- **Fast API**: FastAPI backend with real-time document processing
- **Multiple AI Providers**: Support for Ollama (FREE), OpenAI, and Hugging Face
- **Free Embeddings**: Local sentence-transformers for cost-free vector generation

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

- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RAG
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r backend/requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Install and configure Ollama (recommended)**
   ```bash
   # Download from https://ollama.ai/download
   # After installation:
   ollama serve
   ollama pull phi3:mini
   ```

### Running the System

You need two terminal windows:

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

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AI Provider Selection (ollama, huggingface, openai)
AI_PROVIDER=ollama

# Ollama Configuration (FREE - Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini

# Hugging Face Configuration (FREE - Cloud)
HUGGINGFACE_API_KEY=your_hf_token_here
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

# OpenAI Configuration (PAID)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Embedding Configuration (FREE)
EMBEDDING_PROVIDER=sentence-transformers

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=3
TEMPERATURE=0.7
```

### AI Provider Comparison

| Provider | Cost | Speed | Privacy | Best For |
|----------|------|-------|---------|----------|
| **Ollama** | FREE | Medium | Local | Privacy-focused |
| **Hugging Face** | FREE | Fast | Cloud | Quick setup |
| **OpenAI** | PAID | Very Fast | Cloud | Production use |

## How It Works

### Document Processing Pipeline

1. **Upload**: Documents are uploaded through the web interface
2. **Chunking**: Documents are split into manageable pieces (default: 1000 characters)
3. **Embedding**: Text chunks are converted to numerical vectors
4. **Storage**: Vectors are stored in ChromaDB for fast retrieval
5. **Retrieval**: Questions trigger similarity search for relevant chunks
6. **Generation**: AI generates contextual answers using retrieved information
7. **Response**: Users receive answers with source citations

### Example Workflow

**Scenario**: User uploads a research paper about artificial intelligence

1. **Document Upload**: User uploads "AI_Research_Paper.pdf"
2. **Processing**: System chunks the document and creates embeddings
3. **Question**: User asks "What are the main benefits of AI?"
4. **Retrieval**: System finds relevant chunks about AI benefits
5. **Generation**: AI generates answer using retrieved context
6. **Display**: User sees answer with source citations

## API Endpoints

### System Health
- `GET /api/health` - Check system status
- `GET /api/system-info` - Get system configuration

### Document Management
- `POST /api/upload` - Upload documents
- `GET /api/documents` - List all documents
- `DELETE /api/documents` - Clear all documents
- `POST /api/sample-documents` - Load sample documents

### Chat Interface
- `POST /api/chat` - Ask questions and get AI responses

## Testing the System

### Via API

```bash
# Health check
curl http://localhost:8000/api/health

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'

# Upload a document
curl -X POST http://localhost:8000/api/upload \
  -F "files=@document.pdf"
```

### Via Frontend

1. Navigate to http://localhost:3000
2. Upload documents using the upload interface
3. Ask questions in the chat interface
4. View source citations and document management

## File Format Support

### Supported Formats

- **PDF**: Full text extraction with metadata
- **Text Files**: .txt, .md, .py, .js, .html, .css
- **Documents**: Microsoft Office formats (with additional dependencies)
- **Code Files**: Various programming languages

### Processing Features

- Automatic format detection
- Text extraction and cleaning
- Metadata preservation
- Error handling for corrupted files
- Progress tracking for large files

## Performance Optimization

### Memory Management

- Use smaller models for faster responses (phi3:mini vs llama2)
- Adjust chunk sizes based on available memory
- Monitor memory usage during operation
- Regular cleanup of unused documents

### GPU Acceleration

For NVIDIA GPUs:
```bash
# Install CUDA toolkit
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Storage Considerations

- Vector embeddings stored locally in ChromaDB
- AI models downloaded once and cached
- Document chunks stored as text for quick access
- Regular backup recommended for important data

## System Requirements

### Minimum Requirements

- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or equivalent)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for models and data
- **OS**: Windows 10+, macOS 10.15+, or Linux

### Recommended Requirements

- **CPU**: Intel i7/AMD Ryzen 7 or better
- **RAM**: 16GB or more
- **Storage**: 50GB+ free space for multiple models
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)

## Troubleshooting

### Common Issues

1. **"Ollama not found"**
   - Install Ollama from https://ollama.ai/download
   - Restart computer after installation
   - Run `ollama serve` and `ollama pull phi3:mini`

2. **"Port already in use"**
   - Check what's using the port: `netstat -an | findstr :8000`
   - Kill the process or use different ports

3. **"Module not found"**
   - Reinstall dependencies: `pip install -r requirements.txt`
   - For frontend: `cd frontend && npm install`

4. **Slow responses**
   - Use smaller AI models (phi3:mini instead of llama2)
   - Ensure sufficient RAM (8GB+ recommended)
   - Check if GPU acceleration is available

### Debugging

#### Backend Logs
Monitor the backend terminal for:
- System initialization messages
- Document processing status
- AI model responses
- Error messages and stack traces

#### Frontend Console
Open browser DevTools to see:
- API requests and responses
- Frontend errors and warnings
- Performance metrics
- Network activity

## Development

### Local Development Setup

```bash
# Clone repository
git clone <repository-url>
cd RAG

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Set up environment
cp .env.example .env
# Edit .env with your configuration

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

- **Add document formats**: Modify `backend/document_loader.py`
- **Implement AI providers**: Update `rag_system.py`
- **Create embedding models**: Extend `vector_store.py`
- **Add API endpoints**: Update `backend/main.py`
- **Extend frontend**: Add components in `frontend/components/`

## Security Features

- **Local processing** for sensitive documents (with Ollama)
- **Environment-based configuration** for API keys
- **Input validation** and sanitization
- **CORS configuration** for secure frontend access
- **No data persistence** in external APIs (local mode)

## Advanced Features

### Custom Models

```bash
# Create custom Ollama model
ollama create mymodel -f Modelfile

# Example Modelfile:
FROM phi3:mini
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "You are a helpful assistant specialized in document analysis."
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

## Production Deployment

### Docker Deployment

```dockerfile
# Example Dockerfile for backend
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "backend/run.py"]
```

### Environment Configuration

- Use environment-specific .env files
- Configure proper CORS settings
- Set up SSL/TLS certificates
- Implement proper logging and monitoring

### Scaling Considerations

- Use Redis for session management
- Implement database connection pooling
- Set up load balancing for multiple instances
- Monitor memory and CPU usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at http://localhost:8000/docs
3. Create an issue in the repository
4. Check existing issues for solutions

## Acknowledgments

- Built with LangChain for RAG functionality
- Uses ChromaDB for vector storage
- Frontend powered by Next.js and Tailwind CSS
- Backend built with FastAPI
- AI models provided by Ollama, Hugging Face, and OpenAI