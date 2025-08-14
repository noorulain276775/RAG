from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict, Any
import json
from config import Config

class RAGSystem:
    def __init__(self):
        """Initialize the RAG system with the selected AI provider."""
        self.config = Config()
        self.ai_config = self.config.get_ai_config()
        self.llm = self._initialize_llm()
        self.vector_store = None
        self.document_loader = None
        
        print(f"RAG System initialized with {self.ai_config['provider']} provider")
        if self.ai_config['is_free']:
            print("Using FREE AI provider!")
    
    def _initialize_llm(self):
        """Initialize the language model based on configuration."""
        try:
            if self.ai_config['provider'] == 'ollama':
                # Use Ollama (FREE - runs locally)
                from langchain_community.llms import Ollama
                
                self.llm = Ollama(
                    base_url=self.ai_config['base_url'],
                    model=self.ai_config['model'],
                    temperature=self.config.TEMPERATURE
                )
                print(f"Ollama LLM initialized with model: {self.ai_config['model']}")
                
            elif self.ai_config['provider'] == 'huggingface':
                # Use Hugging Face (FREE tier)
                from langchain_community.llms import HuggingFaceHub
                
                self.llm = HuggingFaceHub(
                    repo_id=self.ai_config['model'],
                    huggingfacehub_api_token=self.ai_config['api_key'],
                    model_kwargs={'temperature': self.config.TEMPERATURE}
                )
                print(f"Hugging Face LLM initialized with model: {self.ai_config['model']}")
                
            else:
                # Use OpenAI (paid)
                from langchain_openai import ChatOpenAI
                
                self.llm = ChatOpenAI(
                    openai_api_key=self.ai_config['api_key'],
                    model_name=self.ai_config['model'],
                    temperature=self.config.TEMPERATURE
                )
                print(f"OpenAI LLM initialized with model: {self.ai_config['model']}")
            
            return self.llm
            
        except Exception as e:
            print(f"❌ Failed to initialize LLM: {e}")
            print("🔄 Falling back to Ollama...")
            
            # Fallback to Ollama
            try:
                from langchain_community.llms import Ollama
                self.llm = Ollama(
                    base_url="http://localhost:11434",
                    model="llama2",
                    temperature=self.config.TEMPERATURE
                )
                print("Fallback to Ollama successful")
                return self.llm
            except Exception as fallback_error:
                print(f"Fallback to Ollama also failed: {fallback_error}")
                raise
    
    def set_components(self, vector_store, document_loader):
        """Set the vector store and document loader components."""
        self.vector_store = vector_store
        self.document_loader = document_loader
        print("RAG components connected")
    
    def query(self, question: str, k: int = None) -> Dict[str, Any]:
        """Query the RAG system with a question."""
        try:
            if not self.vector_store:
                return {"error": "Vector store not initialized"}
            
            # Retrieve relevant documents
            relevant_docs = self.vector_store.similarity_search(question, k=k)
            
            print(f"🔍 Found {len(relevant_docs)} relevant documents for query: '{question[:50]}{'...' if len(question) > 50 else ''}'")
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant documents to answer your question. Please upload some documents first.",
                    "sources": [],
                    "num_sources": 0
                }
            
            # Create context from retrieved documents
            context = self._create_context(relevant_docs)
            
            # Generate answer using the LLM with timeout protection
            try:
                answer = self._generate_answer(question, context)
            except Exception as e:
                if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                    return {
                        "answer": "I'm sorry, but the response is taking too long. Please try asking a simpler question or check if Ollama is running properly.",
                        "sources": [],
                        "num_sources": 0,
                        "error": "timeout"
                    }
                else:
                    raise e
            
            # Extract source information
            sources = self._extract_sources(relevant_docs)
            
            return {
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
            
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return {"error": f"Failed to process query: {str(e)}"}
    
    def _create_context(self, documents: List[Document]) -> str:
        """Create context string from retrieved documents."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}:\n{doc.page_content}")
        
        return "\n\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using the LLM with context."""
        try:
            # Create prompt template
            prompt_template = ChatPromptTemplate.from_template(
                """You are a helpful AI assistant. Use the following context to answer the user's question.
                
                Context:
                {context}
                
                Question: {question}
                
                Instructions:
                1. Answer based ONLY on the provided context
                2. If the context doesn't contain enough information, say so
                3. Be concise but informative
                4. Cite which document(s) you used
                
                Answer:"""
            )
            
            # Create modern LangChain chain
            chain = prompt_template | self.llm | StrOutputParser()
            
            # Generate response with timeout handling
            try:
                response = chain.invoke({"context": context, "question": question})
            except Exception as e:
                print(f"❌ LLM generation error: {e}")
                if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                    return "I'm sorry, but the response is taking too long. Please try asking a simpler question or check if Ollama is running properly."
                else:
                    raise e
            
            return response.strip()
            
        except Exception as e:
            print(f"❌ Failed to generate answer: {e}")
            return f"I encountered an error while generating an answer: {str(e)}"
    
    def _extract_sources(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Extract source information from documents."""
        sources = []
        for i, doc in enumerate(documents):
            source_info = {
                "title": f"Document {i+1}",
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "score": 1.0 - (i * 0.1),  # Simple scoring based on order
                "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
            }
            sources.append(source_info)
        
        return sources
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize text using the LLM."""
        try:
            prompt_template = ChatPromptTemplate.from_template(
                "Please provide a concise summary of the following text in {max_length} words or less:\n\n{text}\n\nSummary:"
            )
            
            chain = prompt_template | self.llm | StrOutputParser()
            summary = chain.invoke({"text": text, "max_length": max_length})
            
            return summary.strip()
            
        except Exception as e:
            print(f"❌ Summarization failed: {e}")
            return f"Failed to summarize text: {str(e)}"
    
    def generate_questions(self, text: str, num_questions: int = 3) -> List[str]:
        """Generate questions about the given text."""
        try:
            prompt_template = ChatPromptTemplate.from_template(
                "Based on the following text, generate {num_questions} interesting questions that someone might ask:\n\n{text}\n\nQuestions:\n1."
            )
            
            chain = prompt_template | self.llm | StrOutputParser()
            response = chain.invoke({"text": text, "num_questions": num_questions})
            
            # Parse questions from response
            questions = []
            lines = response.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('1.', '2.', '3.', '4.', '5.')) or line.startswith('-')):
                    question = line.split('.', 1)[1].strip() if '.' in line else line[1:].strip()
                    if question:
                        questions.append(question)
            
            return questions[:num_questions]
            
        except Exception as e:
            print(f"❌ Question generation failed: {e}")
            return [f"Failed to generate questions: {str(e)}"]
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and configuration."""
        return {
            "ai_provider": self.ai_config['provider'],
            "ai_model": self.ai_config['model'],
            "is_free": self.ai_config['is_free'],
            "embedding_provider": self.config.get_embedding_config()['provider'],
            "embedding_model": self.config.get_embedding_config()['model'],
            "chunk_size": self.config.CHUNK_SIZE,
            "chunk_overlap": self.config.CHUNK_OVERLAP,
            "temperature": self.config.TEMPERATURE,
            "vector_store_ready": self.vector_store is not None,
            "document_loader_ready": self.document_loader is not None
        }
