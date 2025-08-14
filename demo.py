#!/usr/bin/env python3
"""
Demo script for the RAG System
Shows the system in action with a simple example.
"""

import os
import time
from document_loader import DocumentLoader
from vector_store import VectorStore
from rag_system import RAGSystem

def print_header():
    """Print a nice header for the demo."""
    print("🤖" + "="*60 + "🤖")
    print("           RAG SYSTEM DEMONSTRATION")
    print("🤖" + "="*60 + "🤖")
    print()

def print_step(step_num, title, description=""):
    """Print a step header."""
    print(f"\n{step_num}️⃣ {title}")
    if description:
        print(f"   {description}")
    print("   " + "-" * 50)

def demo_basic_rag():
    """Demonstrate basic RAG functionality."""
    print_header()
    
    # Step 1: Initialize the system
    print_step(1, "Initializing RAG System", "Setting up document loader, vector store, and AI components...")
    
    try:
        loader = DocumentLoader()
        vector_store = VectorStore()
        rag_system = RAGSystem()
        print("   ✅ RAG system initialized successfully!")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        print("   💡 Make sure you have set your OpenAI API key in the .env file")
        return False
    
    # Step 2: Load sample documents
    print_step(2, "Loading Sample Documents", "Creating sample AI/ML content for demonstration...")
    
    try:
        sample_docs = loader.create_sample_documents()
        if sample_docs:
            success = vector_store.add_documents(sample_docs)
            if success:
                print(f"   ✅ Loaded {len(sample_docs)} document chunks!")
                print("   📚 Sample content includes AI, Machine Learning, and RAG topics")
            else:
                print("   ❌ Failed to add documents to vector store")
                return False
        else:
            print("   ❌ Failed to create sample documents")
            return False
    except Exception as e:
        print(f"   ❌ Error loading documents: {e}")
        return False
    
    # Step 3: Show system information
    print_step(3, "System Information", "Displaying current configuration and statistics...")
    
    try:
        system_info = rag_system.get_system_info()
        print(f"   🤖 AI Model: {system_info['model']}")
        print(f"   🌡️  Temperature: {system_info['temperature']}")
        print(f"   📏 Chunk Size: {system_info['chunk_size']} characters")
        print(f"   🔗 Chunk Overlap: {system_info['chunk_overlap']} characters")
        print(f"   🎯 Top K Results: {system_info['top_k_results']}")
        
        if 'vector_store_stats' in system_info:
            stats = system_info['vector_store_stats']
            print(f"   📊 Total Documents: {stats.get('total_documents', 'Unknown')}")
            print(f"   🧠 Embedding Model: {stats.get('embedding_model', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Error getting system info: {e}")
    
    # Step 4: Interactive Q&A session
    print_step(4, "Interactive Q&A Session", "Ask questions about the loaded content...")
    
    demo_questions = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What is the difference between AI and ML?",
        "Explain RAG systems in simple terms",
        "What are embeddings and why are they useful?"
    ]
    
    print("   💡 Demo questions will be asked automatically...")
    time.sleep(1)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n   🤔 Question {i}: {question}")
        print("   " + "─" * 60)
        
        try:
            # Add a small delay to make the demo more readable
            time.sleep(0.5)
            
            response = rag_system.query(question)
            
            if response.get('error'):
                print(f"      ❌ Error: {response['error']}")
            else:
                print(f"      🤖 Answer: {response['answer']}")
                print(f"      📚 Sources: {response['num_sources']} documents")
                
                # Show source previews
                if response.get('sources'):
                    print("      📖 Source previews:")
                    for j, source in enumerate(response['sources'][:2], 1):  # Show first 2 sources
                        source_name = source.get('metadata', {}).get('source', 'Unknown')
                        content_preview = source['content'][:80] + "..." if len(source['content']) > 80 else source['content']
                        print(f"         {j}. {source_name}: {content_preview}")
                
        except Exception as e:
            print(f"      ❌ Error processing question: {e}")
        
        print()
        time.sleep(1)  # Pause between questions
    
    # Step 5: Additional features demonstration
    print_step(5, "Additional Features", "Showing text summarization and question generation...")
    
    # Text summarization
    print("   📝 Text Summarization Demo:")
    sample_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create 
    intelligent machines that work and react like humans. Machine Learning is a subset 
    of AI that enables computers to learn and improve from experience without being 
    explicitly programmed. Deep Learning uses neural networks with multiple layers to 
    model and understand complex patterns in data. Natural Language Processing (NLP) 
    is a field of AI that focuses on the interaction between computers and human language.
    """
    
    try:
        summary = rag_system.summarize_text(sample_text)
        print(f"      📄 Original text: {len(sample_text)} characters")
        print(f"      ✨ Summary: {summary}")
    except Exception as e:
        print(f"      ❌ Error generating summary: {e}")
    
    # Question generation
    print("\n   ❓ Question Generation Demo:")
    try:
        questions = rag_system.generate_questions(sample_text)
        print(f"      📝 Generated questions:\n{questions}")
    except Exception as e:
        print(f"      ❌ Error generating questions: {e}")
    
    # Step 6: Vector search demonstration
    print_step(6, "Vector Search Demo", "Showing how similarity search works...")
    
    try:
        query = "neural networks and deep learning"
        print(f"   🔍 Searching for: '{query}'")
        
        results_with_scores = vector_store.similarity_search_with_score(query, k=3)
        
        if results_with_scores:
            print(f"   📊 Found {len(results_with_scores)} relevant results:")
            
            for i, (doc, score) in enumerate(results_with_scores, 1):
                print(f"      {i}. Similarity Score: {score:.4f}")
                print(f"         Content: {doc.page_content[:100]}...")
                print(f"         Source: {doc.metadata.get('source', 'Unknown')}")
                print()
        else:
            print("   ❌ No results found")
            
    except Exception as e:
        print(f"   ❌ Error in vector search: {e}")
    
    # Step 7: Cleanup and conclusion
    print_step(7, "Demo Conclusion", "Cleaning up and showing next steps...")
    
    try:
        # Clear the vector store
        if vector_store.clear_collection():
            print("   🧹 Vector store cleared successfully")
        else:
            print("   ⚠️  Could not clear vector store")
    except Exception as e:
        print(f"   ⚠️  Error during cleanup: {e}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 What you've seen:")
    print("   ✅ Document loading and chunking")
    print("   ✅ Vector embeddings and storage")
    print("   ✅ Semantic search and retrieval")
    print("   ✅ AI-powered question answering")
    print("   ✅ Source attribution and transparency")
    print("   ✅ Text summarization and question generation")
    
    print("\n🚀 Next steps:")
    print("   - Try the web interface: streamlit run streamlit_app.py")
    print("   - Use the CLI: python cli_app.py")
    print("   - Upload your own documents")
    print("   - Customize the configuration")
    
    return True

def main():
    """Main demo function."""
    try:
        success = demo_basic_rag()
        if success:
            print("\n🌟 Demo completed! The RAG system is working correctly.")
        else:
            print("\n❌ Demo failed. Please check the errors above.")
            print("💡 Make sure you have:")
            print("   - Python 3.8+ installed")
            print("   - All dependencies installed (pip install -r requirements.txt)")
            print("   - OpenAI API key set in .env file")
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during demo: {e}")

if __name__ == "__main__":
    main()
