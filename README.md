# 🤖 RAG System - AI-Powered Document Q&A

A comprehensive **Retrieval-Augmented Generation (RAG)** system with a modern Next.js frontend and Python backend. Upload documents and ask questions with AI-powered context awareness.

## 🚀 **Features**

- **📄 Document Upload**: Support for PDF, TXT, DOC, Markdown, and code files
- **🧠 AI-Powered Q&A**: Ask questions about your documents with full context
- **🔍 Smart Retrieval**: Vector-based similarity search for relevant content
- **💬 Interactive Chat**: Modern chat interface with source citations
- **📱 Responsive Design**: Beautiful Next.js frontend with Tailwind CSS
- **⚡ Fast API**: FastAPI backend with real-time document processing
- **🔐 Secure**: OpenAI API integration with environment-based configuration

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI       │    │   RAG System    │
│   Frontend      │◄──►│   Backend       │◄──►│   (Python)      │
│   (Port 3000)   │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 **Project Structure**

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
├── document_loader.py        # Document Processing
├── vector_store.py          # Vector Database
├── rag_system.py            # Core RAG Logic
├── config.py                # Configuration
├── requirements.txt          # Python Dependencies
└── README.md                # This File
```

## 🛠️ **Quick Start**

### **1. Setup Environment**

```bash
# Clone or navigate to project directory
cd RAG

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your_actual_key_here" > .env
```

### **2. Install Python Dependencies**

```bash
# Install Python packages
pip install -r requirements.txt

# Install backend dependencies
pip install -r backend/requirements.txt
```

### **3. Start Backend**

```bash
# Start FastAPI backend
cd backend
python run.py
```

**Backend will be available at:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### **4. Start Frontend**

```bash
# In a new terminal, install frontend dependencies
cd frontend
npm install

# Start Next.js development server
npm run dev
```

**Frontend will be available at:** http://localhost:3000

## 🎯 **How It Works**

### **Document Processing Pipeline:**

1. **📤 Upload**: Drag & drop or select files through the web interface
2. **✂️ Chunking**: Documents are split into smaller, manageable pieces
3. **🔢 Embedding**: Text chunks are converted to numerical vectors using OpenAI
4. **💾 Storage**: Vectors are stored in ChromaDB for fast retrieval
5. **🔍 Retrieval**: When you ask a question, relevant chunks are found
6. **🤖 Generation**: AI generates answers using retrieved context

### **Context Awareness:**

- **Before**: AI gives generic answers
- **After**: AI provides specific, document-based responses with sources

## 📱 **Frontend Features**

### **Main Interface:**
- **Chat Tab**: Interactive Q&A with your documents
- **Documents Tab**: Manage uploaded files
- **Settings Tab**: Configure API keys and models

### **Document Upload:**
- Drag & drop support
- Multiple file selection
- Progress indicators
- File type validation

### **Chat Interface:**
- Real-time messaging
- Source citations
- Copy responses
- Loading states

## 🔌 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/upload` | POST | Upload documents |
| `/api/chat` | POST | Ask questions |
| `/api/documents` | GET | List documents |
| `/api/sample-documents` | POST | Load sample data |
| `/api/system-info` | GET | System configuration |

## 🧪 **Testing the System**

### **1. Load Sample Documents**
```bash
# Via API
curl -X POST http://localhost:8000/api/sample-documents

# Via Frontend
# Go to Documents tab → Click "Load Sample Documents"
```

### **2. Ask Questions**
```bash
# Via API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the difference between AI and ML?"}'

# Via Frontend
# Go to Chat tab → Type your question
```

## ⚙️ **Configuration**

### **Environment Variables (.env):**
```env
OPENAI_API_KEY=sk-your_actual_key_here
OPENAI_MODEL=gpt-3.5-turbo
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=3
TEMPERATURE=0.7
```

### **Frontend Configuration:**
- API endpoint: `http://localhost:8000`
- CORS enabled for development
- Responsive design with Tailwind CSS

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"OpenAI API key not found"**
   - Create `.env` file in project root
   - Add your actual OpenAI API key

2. **"Module not found" errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Install backend deps: `pip install -r backend/requirements.txt`

3. **Frontend can't connect to backend**
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify API endpoints

4. **Documents not processing**
   - Check file format support
   - Verify OpenAI API key is valid
   - Check backend logs for errors

### **Debug Mode:**
```bash
# Backend with verbose logging
cd backend
python run.py --log-level debug

# Frontend with detailed errors
cd frontend
npm run dev
```

## 🔮 **Future Enhancements**

- [ ] **User Authentication**: Secure document access
- [ ] **Document Versioning**: Track document changes
- [ ] **Advanced Search**: Filters and sorting
- [ ] **Export Features**: Download processed documents
- [ ] **Real-time Updates**: WebSocket notifications
- [ ] **Mobile App**: React Native version

## 📚 **Learning Resources**

- **RAG Concepts**: [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- **Next.js**: [Official Documentation](https://nextjs.org/docs)
- **FastAPI**: [User Guide](https://fastapi.tiangolo.com/)
- **Vector Databases**: [ChromaDB Docs](https://docs.trychroma.com/)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

## 🆘 **Support**

- **Issues**: Create a GitHub issue
- **Questions**: Check the troubleshooting section
- **Documentation**: Review API docs at `/docs` endpoint

---

**Happy Document Q&A! 🎉**

*Built with ❤️ using Next.js, FastAPI, and OpenAI*
