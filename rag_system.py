from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.chains import LLMChain
from vector_store import VectorStore
from config import Config

class RAGSystem:
    """Main RAG system that combines retrieval and generation."""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            model_name=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE
        )
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Setup the prompt templates for different RAG operations."""
        
        # Main RAG prompt template
        self.rag_prompt = ChatPromptTemplate.from_template(
            """You are a helpful AI assistant that answers questions based on the provided context.
            
            Context information:
            {context}
            
            Question: {question}
            
            Instructions:
            1. Answer the question based ONLY on the context provided above
            2. If the context doesn't contain enough information to answer the question, say "I don't have enough information to answer this question based on the provided context."
            3. Be concise but comprehensive
            4. Use the context to provide accurate and relevant answers
            5. If you're unsure about something, acknowledge the uncertainty
            
            Answer:"""
        )
        
        # Summarization prompt template
        self.summary_prompt = ChatPromptTemplate.from_template(
            """Please provide a concise summary of the following text:
            
            {text}
            
            Summary:"""
        )
        
        # Question generation prompt template
        self.question_prompt = ChatPromptTemplate.from_template(
            """Based on the following context, generate 3 relevant questions that could be asked:
            
            Context: {context}
            
            Generate 3 questions that would help someone understand this topic better:"""
        )
    
    def query(self, question: str, k: int = None) -> Dict[str, Any]:
        """Main RAG query method that retrieves relevant documents and generates an answer."""
        try:
            # Step 1: Retrieve relevant documents
            relevant_docs = self.vector_store.similarity_search(question, k=k)
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "sources": [],
                    "context": "",
                    "error": "No relevant documents found"
                }
            
            # Step 2: Prepare context from retrieved documents
            context = self._prepare_context(relevant_docs)
            
            # Step 3: Generate answer using LLM
            chain = LLMChain(llm=self.llm, prompt=self.rag_prompt)
            response = chain.run(context=context, question=question)
            
            # Step 4: Prepare sources information
            sources = self._extract_sources(relevant_docs)
            
            return {
                "answer": response.strip(),
                "sources": sources,
                "context": context,
                "num_sources": len(relevant_docs)
            }
            
        except Exception as e:
            return {
                "answer": f"An error occurred while processing your question: {str(e)}",
                "sources": [],
                "context": "",
                "error": str(e)
            }
    
    def query_with_scores(self, question: str, k: int = None) -> Dict[str, Any]:
        """Query with similarity scores for analysis."""
        try:
            # Retrieve documents with scores
            results_with_scores = self.vector_store.similarity_search_with_score(question, k=k)
            
            if not results_with_scores:
                return {
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "sources": [],
                    "context": "",
                    "scores": [],
                    "error": "No relevant documents found"
                }
            
            # Separate documents and scores
            relevant_docs = [doc for doc, score in results_with_scores]
            scores = [score for doc, score in results_with_scores]
            
            # Prepare context and generate answer
            context = self._prepare_context(relevant_docs)
            chain = LLMChain(llm=self.llm, prompt=self.rag_prompt)
            response = chain.run(context=context, question=question)
            
            # Prepare sources with scores
            sources = self._extract_sources_with_scores(relevant_docs, scores)
            
            return {
                "answer": response.strip(),
                "sources": sources,
                "context": context,
                "scores": scores,
                "num_sources": len(relevant_docs)
            }
            
        except Exception as e:
            return {
                "answer": f"An error occurred while processing your question: {str(e)}",
                "sources": [],
                "context": "",
                "scores": [],
                "error": str(e)
            }
    
    def summarize_text(self, text: str) -> str:
        """Summarize a given text using the LLM."""
        try:
            chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
            response = chain.run(text=text)
            return response.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_questions(self, context: str) -> str:
        """Generate relevant questions based on given context."""
        try:
            chain = LLMChain(llm=self.llm, prompt=self.question_prompt)
            response = chain.run(context=context)
            return response.strip()
        except Exception as e:
            return f"Error generating questions: {str(e)}"
    
    def _prepare_context(self, documents: List[Document]) -> str:
        """Prepare context string from retrieved documents."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', f'Document {i}')
            content = doc.page_content.strip()
            context_parts.append(f"Source {i} ({source}):\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _extract_sources(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Extract source information from documents."""
        sources = []
        for doc in documents:
            source_info = {
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata,
                "length": len(doc.page_content)
            }
            sources.append(source_info)
        return sources
    
    def _extract_sources_with_scores(self, documents: List[Document], scores: List[float]) -> List[Dict[str, Any]]:
        """Extract source information with similarity scores."""
        sources = []
        for doc, score in zip(documents, scores):
            source_info = {
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata,
                "length": len(doc.page_content),
                "similarity_score": float(score)
            }
            sources.append(source_info)
        return sources
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the RAG system."""
        vector_stats = self.vector_store.get_collection_stats()
        
        return {
            "model": Config.OPENAI_MODEL,
            "temperature": Config.TEMPERATURE,
            "chunk_size": Config.CHUNK_SIZE,
            "chunk_overlap": Config.CHUNK_OVERLAP,
            "top_k_results": Config.TOP_K_RESULTS,
            "vector_store_stats": vector_stats
        }
