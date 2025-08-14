import streamlit as st
import os
import tempfile
from typing import List
import json

from document_loader import DocumentLoader
from vector_store import VectorStore
from rag_system import RAGSystem
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .source-box {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ff7f0e;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'document_loader' not in st.session_state:
        st.session_state.document_loader = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def initialize_components():
    """Initialize RAG system components."""
    try:
        if st.session_state.rag_system is None:
            with st.spinner("Initializing RAG system..."):
                st.session_state.document_loader = DocumentLoader()
                st.session_state.vector_store = VectorStore()
                st.session_state.rag_system = RAGSystem()
            st.success("RAG system initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing RAG system: {str(e)}")
        st.info("Please check your OpenAI API key in the configuration.")

def main():
    """Main application function."""
    st.markdown('<h1 class="main-header">🤖 AI RAG System</h1>', unsafe_allow_html=True)
    
    # Initialize session state and components
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🚀 Quick Start")
        
        if st.button("Initialize RAG System", type="primary"):
            initialize_components()
        
        st.markdown("---")
        
        st.markdown("## 📚 Document Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['pdf', 'txt', 'md', 'py', 'js', 'html', 'css'],
            accept_multiple_files=True,
            help="Upload multiple files to add to the knowledge base"
        )
        
        if uploaded_files and st.button("Process Documents"):
            if st.session_state.document_loader:
                process_uploaded_files(uploaded_files)
            else:
                st.error("Please initialize the RAG system first!")
        
        # Sample documents
        if st.button("Load Sample Documents"):
            if st.session_state.document_loader:
                load_sample_documents()
            else:
                st.error("Please initialize the RAG system first!")
        
        st.markdown("---")
        
        st.markdown("## ⚙️ Settings")
        
        # Configuration display
        if st.session_state.rag_system:
            config = st.session_state.rag_system.get_system_info()
            st.json(config)
        
        # Clear vector store
        if st.button("Clear Knowledge Base", type="secondary"):
            if st.session_state.vector_store:
                if st.session_state.vector_store.clear_collection():
                    st.success("Knowledge base cleared!")
                    st.session_state.chat_history = []
                else:
                    st.error("Failed to clear knowledge base")
    
    # Main content area
    if st.session_state.rag_system is None:
        st.info("👈 Please initialize the RAG system from the sidebar to get started!")
        return
    
    # Chat interface
    st.markdown('<h2 class="sub-header">💬 Ask Questions</h2>', unsafe_allow_html=True)
    
    # Chat input
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        # Add user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Get RAG response
        with st.spinner("Thinking..."):
            response = st.session_state.rag_system.query(user_question)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                
                # Show sources if available
                if st.session_state.chat_history and len(st.session_state.chat_history) > 0:
                    last_response = st.session_state.rag_system.query(
                        st.session_state.chat_history[-2]["content"]
                    ) if len(st.session_state.chat_history) >= 2 else None
                    
                    if last_response and "sources" in last_response and last_response["sources"]:
                        with st.expander("📖 View Sources"):
                            for i, source in enumerate(last_response["sources"]):
                                st.markdown(f"**Source {i+1}:**")
                                st.markdown(f"*{source.get('metadata', {}).get('source', 'Unknown')}*")
                                st.markdown(f"```\n{source['content']}\n```")
                                st.markdown("---")
    
    # Additional features
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">📝 Text Summarization</h3>', unsafe_allow_html=True)
        text_to_summarize = st.text_area("Enter text to summarize:", height=150)
        if st.button("Summarize"):
            if text_to_summarize:
                with st.spinner("Generating summary..."):
                    summary = st.session_state.rag_system.summarize_text(text_to_summarize)
                    st.markdown("**Summary:**")
                    st.write(summary)
    
    with col2:
        st.markdown('<h3 class="sub-header">❓ Question Generation</h3>', unsafe_allow_html=True)
        context_for_questions = st.text_area("Enter context to generate questions from:", height=150)
        if st.button("Generate Questions"):
            if context_for_questions:
                with st.spinner("Generating questions..."):
                    questions = st.session_state.rag_system.generate_questions(context_for_questions)
                    st.markdown("**Generated Questions:**")
                    st.write(questions)

def process_uploaded_files(uploaded_files):
    """Process uploaded files and add them to the vector store."""
    try:
        total_docs = 0
        
        for uploaded_file in uploaded_files:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Load and process the file
                documents = st.session_state.document_loader.load_file(tmp_file_path)
                
                if documents:
                    # Add to vector store
                    success = st.session_state.vector_store.add_documents(documents)
                    if success:
                        total_docs += len(documents)
                        st.success(f"✅ Processed {uploaded_file.name}: {len(documents)} chunks")
                    else:
                        st.error(f"❌ Failed to add {uploaded_file.name} to vector store")
                else:
                    st.warning(f"⚠️ No content extracted from {uploaded_file.name}")
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
        
        if total_docs > 0:
            st.success(f"🎉 Successfully processed {total_docs} document chunks!")
            st.balloons()
        
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")

def load_sample_documents():
    """Load sample documents for testing."""
    try:
        with st.spinner("Loading sample documents..."):
            sample_docs = st.session_state.document_loader.create_sample_documents()
            
            if sample_docs:
                success = st.session_state.vector_store.add_documents(sample_docs)
                if success:
                    st.success(f"✅ Loaded {len(sample_docs)} sample document chunks!")
                    st.info("You can now ask questions about AI, Machine Learning, and RAG systems!")
                else:
                    st.error("❌ Failed to add sample documents to vector store")
            else:
                st.error("❌ Failed to create sample documents")
                
    except Exception as e:
        st.error(f"Error loading sample documents: {str(e)}")

if __name__ == "__main__":
    main()
