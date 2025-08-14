# 🦙 Ollama Setup Guide - FREE AI for RAG System

## 🎯 **What is Ollama?**

**Ollama** is a free, open-source tool that runs large language models **locally on your computer**. No API costs, no rate limits, no internet required after setup!

## 🆓 **Why Ollama is Perfect for RAG:**

- ✅ **100% FREE** - No hidden costs
- ✅ **Runs Locally** - Your data stays on your computer
- ✅ **Multiple Models** - Llama 2, Mistral, CodeLlama, etc.
- ✅ **Fast Performance** - GPU acceleration support
- ✅ **Privacy First** - No data sent to external servers

## 🚀 **Quick Setup (Windows)**

### **Step 1: Download Ollama**
1. Go to [https://ollama.ai/download](https://ollama.ai/download)
2. Download the **Windows installer**
3. Run the installer and follow the prompts
4. **Restart your computer** after installation

### **Step 2: Verify Installation**
Open a new terminal and run:
```bash
ollama --version
```
You should see something like: `ollama version 0.1.0`

### **Step 3: Download Your First Model**
```bash
# Download Llama 2 (recommended for RAG)
ollama pull llama2

# Or try Mistral (faster, smaller)
ollama pull mistral

# Or CodeLlama (great for technical documents)
ollama pull codellama
```

### **Step 4: Test Ollama**
```bash
# Test the model
ollama run llama2 "Hello! Can you help me with a question?"
```

## 🖥️ **Alternative: Docker Setup**

If you prefer Docker:
```bash
# Pull Ollama Docker image
docker pull ollama/ollama

# Run Ollama container
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Download model
docker exec -it ollama ollama pull llama2
```

## ⚙️ **Configuration**

### **Environment Variables (.env)**
```env
# AI Provider Selection
AI_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Embedding Configuration (FREE)
EMBEDDING_PROVIDER=sentence-transformers

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=3
TEMPERATURE=0.7
```

### **Available Models**
| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama2` | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | General RAG |
| `mistral` | 7B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Fast responses |
| `codellama` | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Technical docs |
| `llama2:13b` | 13B | ⚡⚡ | ⭐⭐⭐⭐⭐ | High quality |
| `llama2:70b` | 70B | ⚡ | ⭐⭐⭐⭐⭐⭐ | Best quality |

## 🧪 **Testing Your Setup**

### **1. Start Ollama Service**
```bash
# Start Ollama (it runs in background)
ollama serve
```

### **2. Test Model Download**
```bash
# Download a model
ollama pull llama2

# Test the model
ollama run llama2 "What is artificial intelligence?"
```

### **3. Test RAG System**
```bash
# Start your RAG backend
cd backend
python run.py
```

### **4. Check Health**
Visit: http://localhost:8000/api/health

You should see:
```json
{
  "status": "healthy",
  "ai_provider": "ollama",
  "ai_model": "llama2",
  "is_free": true
}
```

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Ollama not found"**
   - Restart your computer after installation
   - Check if Ollama is in your PATH

2. **"Connection refused"**
   - Make sure Ollama is running: `ollama serve`
   - Check if port 11434 is available

3. **"Model not found"**
   - Download the model: `ollama pull llama2`
   - Check available models: `ollama list`

4. **Slow responses**
   - Use smaller models (7B instead of 13B/70B)
   - Enable GPU acceleration if available

### **Performance Tips:**

- **GPU Acceleration**: Install CUDA for NVIDIA GPUs
- **Model Selection**: Start with 7B models for speed
- **Memory**: Ensure 8GB+ RAM available
- **Storage**: Models are 4-40GB each

## 🌟 **Advanced Features**

### **Custom Models**
```bash
# Create custom model with specific parameters
ollama create mymodel -f Modelfile

# Modelfile example:
FROM llama2
PARAMETER temperature 0.7
PARAMETER top_p 0.9
```

### **Model Management**
```bash
# List installed models
ollama list

# Remove unused models
ollama rm llama2:13b

# Show model info
ollama show llama2
```

## 📊 **Performance Comparison**

| Provider | Cost | Speed | Quality | Privacy |
|----------|------|-------|---------|---------|
| **Ollama** | 🆓 FREE | ⚡⚡⚡ | ⭐⭐⭐⭐ | 🔒 100% |
| OpenAI | 💰 $0.002/1K tokens | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 🔓 API |
| Hugging Face | 🆓 Free tier | ⚡⚡ | ⭐⭐⭐ | 🔓 API |

## 🎉 **You're Ready!**

Once Ollama is running:
1. ✅ **AI is FREE** - No more API costs!
2. ✅ **Runs Locally** - Your data stays private
3. ✅ **High Quality** - Professional-grade responses
4. ✅ **Always Available** - No internet dependency

## 🚀 **Next Steps**

1. **Start Ollama**: `ollama serve`
2. **Download Model**: `ollama pull llama2`
3. **Start RAG System**: `python backend/run.py`
4. **Test Frontend**: `npm run dev` (in frontend folder)
5. **Upload Documents** and start asking questions!

---

**Happy FREE AI-ing! 🦙✨**

*Questions? Check the troubleshooting section or create an issue on GitHub.*
