# 🤖 AI RAG System

A powerful **Retrieval-Augmented Generation (RAG)** system built with Python, combining document processing, vector search, and AI-powered question answering.

## ✨ Features

- **📚 Multi-format Document Support**: PDF, TXT, MD, Python, JavaScript, HTML, CSS
- **🔍 Vector-based Search**: ChromaDB with OpenAI embeddings for semantic search
- **🤖 AI-powered Responses**: OpenAI GPT models for intelligent question answering
- **💻 Multiple Interfaces**: Web UI (Streamlit) and Command Line Interface
- **📊 Document Chunking**: Intelligent text splitting with configurable overlap
- **🎯 Source Attribution**: Always see where answers come from
- **⚡ Fast & Efficient**: Optimized for performance and scalability

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd RAG

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 3. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### 4. Run the System

#### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

#### Command Line Interface
```bash
# Interactive mode
python cli_app.py

# Single query
python cli_app.py -q "What is artificial intelligence?"

# Load documents
python cli_app.py -f document1.pdf document2.txt

# Load sample documents
python cli_app.py --sample
```

## 🎯 How It Works

### 1. **Document Processing**
- Documents are loaded and chunked into smaller pieces
- Each chunk maintains context with configurable overlap
- Metadata is preserved for source tracking

### 2. **Vector Embeddings**
- Text chunks are converted to high-dimensional vectors
- OpenAI's `text-embedding-ada-002` model creates semantic representations
- Vectors are stored in ChromaDB for fast similarity search

### 3. **Retrieval**
- User questions are converted to query vectors
- Similarity search finds the most relevant document chunks
- Top-k results are selected based on semantic similarity

### 4. **Generation**
- Retrieved chunks provide context for the AI model
- OpenAI GPT generates accurate, contextual answers
- Sources are tracked and displayed for transparency

## 📁 Project Structure

```
RAG/
├── config.py              # Configuration management
├── document_loader.py     # Document processing and chunking
├── vector_store.py        # Vector database operations
├── rag_system.py          # Core RAG logic
├── streamlit_app.py       # Web interface
├── cli_app.py            # Command line interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `CHUNK_SIZE` | 1000 | Number of characters per document chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between consecutive chunks |
| `TOP_K_RESULTS` | 3 | Number of relevant documents to retrieve |
| `TEMPERATURE` | 0.7 | AI model creativity (0.0 = focused, 1.0 = creative) |

## 💡 Usage Examples

### Web Interface
1. Open the Streamlit app
2. Click "Initialize RAG System"
3. Upload documents or load sample data
4. Ask questions in the chat interface
5. View sources and system statistics

### Command Line
```bash
# Initialize and check stats
python cli_app.py --init

# Load documents and start chatting
python cli_app.py -f my_documents.pdf
# Then type questions interactively

# Quick single question
python cli_app.py -q "What are the main benefits of RAG?"
```

## 🛠️ Advanced Features

### Custom Document Types
The system automatically detects file types and uses appropriate loaders:
- **PDF**: PyPDF loader with text extraction
- **Text**: Direct text loading with encoding support
- **Code**: Syntax-aware processing for programming languages
- **Other**: Unstructured loader for various formats

### Vector Store Management
- Persistent storage with ChromaDB
- Automatic collection management
- Document deletion and clearing capabilities
- Performance statistics and monitoring

### Prompt Engineering
- Configurable prompt templates
- Context-aware question answering
- Source attribution and transparency
- Customizable response generation

## 🔍 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Ensure your `.env` file exists and contains the API key
   - Check that the key is valid and has sufficient credits

2. **"No relevant documents found"**
   - Load documents first using the file uploader or CLI
   - Try the "Load Sample Documents" feature to test the system

3. **"Vector store initialization failed"**
   - Check disk space and permissions
   - Try clearing the `./chroma_db` directory

4. **Slow performance**
   - Reduce `CHUNK_SIZE` for faster processing
   - Use smaller documents or fewer files
   - Check your internet connection for API calls

### Performance Tips

- **Chunk Size**: Smaller chunks (500-1000) for precise answers, larger (1500-2000) for context
- **Overlap**: 10-20% overlap maintains context between chunks
- **Document Types**: Text files process faster than PDFs
- **Batch Processing**: Upload multiple documents at once for efficiency

## 🚀 Deployment

### Local Development
```bash
# Install in development mode
pip install -e .

# Run with auto-reload
streamlit run streamlit_app.py --server.runOnSave true
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export OPENAI_API_KEY=your_production_key
export CHROMA_PERSIST_DIRECTORY=/data/chroma_db

# Run with production settings
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for the GPT models and embeddings
- **LangChain** for the RAG framework
- **ChromaDB** for vector storage
- **Streamlit** for the web interface

## 📞 Support

- **Issues**: Create a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check this README and code comments

---

**Happy RAG-ing! 🎉**

*Built with ❤️ using Python, LangChain, and OpenAI*
