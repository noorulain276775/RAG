#!/usr/bin/env python3
"""
Example usage of the RAG System
This script demonstrates how to use the RAG system programmatically.
"""

import os
from document_loader import DocumentLoader
from vector_store import VectorStore
from rag_system import RAGSystem
from config import Config

def main():
    """Demonstrate the RAG system capabilities."""
    
    print("🚀 RAG System Example Usage")
    print("=" * 50)
    
    # Step 1: Initialize components
    print("\n1️⃣ Initializing RAG System...")
    try:
        document_loader = DocumentLoader()
        vector_store = VectorStore()
        rag_system = RAGSystem()
        print("✅ All components initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        print("💡 Make sure you have set your OpenAI API key in the .env file")
        return
    
    # Step 2: Load sample documents
    print("\n2️⃣ Loading sample documents...")
    try:
        sample_docs = document_loader.create_sample_documents()
        if sample_docs:
            success = vector_store.add_documents(sample_docs)
            if success:
                print(f"✅ Loaded {len(sample_docs)} sample document chunks!")
            else:
                print("❌ Failed to add documents to vector store")
                return
        else:
            print("❌ Failed to create sample documents")
            return
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return
    
    # Step 3: Show system information
    print("\n3️⃣ System Information:")
    try:
        system_info = rag_system.get_system_info()
        print(f"   Model: {system_info['model']}")
        print(f"   Temperature: {system_info['temperature']}")
        print(f"   Chunk Size: {system_info['chunk_size']}")
        print(f"   Chunk Overlap: {system_info['chunk_overlap']}")
        print(f"   Top K Results: {system_info['top_k_results']}")
        
        if 'vector_store_stats' in system_info:
            stats = system_info['vector_store_stats']
            print(f"   Total Documents: {stats.get('total_documents', 'Unknown')}")
            print(f"   Embedding Model: {stats.get('embedding_model', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error getting system info: {e}")
    
    # Step 4: Demonstrate RAG queries
    print("\n4️⃣ Testing RAG Queries:")
    
    test_questions = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What is the difference between AI and ML?",
        "Explain RAG systems",
        "What are embeddings used for?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Question {i}: {question}")
        try:
            response = rag_system.query(question)
            
            if response.get('error'):
                print(f"      ❌ Error: {response['error']}")
            else:
                print(f"      🤖 Answer: {response['answer'][:150]}...")
                print(f"      📚 Sources: {response['num_sources']} documents")
                
                # Show first source preview
                if response.get('sources'):
                    first_source = response['sources'][0]
                    source_name = first_source.get('metadata', {}).get('source', 'Unknown')
                    print(f"      📖 First source: {source_name}")
                    
        except Exception as e:
            print(f"      ❌ Error processing question: {e}")
    
    # Step 5: Demonstrate additional features
    print("\n5️⃣ Additional Features:")
    
    # Text summarization
    print("\n   📝 Text Summarization:")
    sample_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create 
    intelligent machines that work and react like humans. Machine Learning is a subset 
    of AI that enables computers to learn and improve from experience without being 
    explicitly programmed. Deep Learning uses neural networks with multiple layers to 
    model and understand complex patterns in data.
    """
    
    try:
        summary = rag_system.summarize_text(sample_text)
        print(f"      Original length: {len(sample_text)} characters")
        print(f"      Summary: {summary}")
    except Exception as e:
        print(f"      ❌ Error generating summary: {e}")
    
    # Question generation
    print("\n   ❓ Question Generation:")
    try:
        questions = rag_system.generate_questions(sample_text)
        print(f"      Generated questions:\n{questions}")
    except Exception as e:
        print(f"      ❌ Error generating questions: {e}")
    
    # Step 6: Vector store operations
    print("\n6️⃣ Vector Store Operations:")
    
    try:
        # Similarity search with scores
        query = "neural networks"
        results_with_scores = vector_store.similarity_search_with_score(query, k=2)
        
        print(f"   Query: '{query}'")
        print(f"   Found {len(results_with_scores)} results:")
        
        for i, (doc, score) in enumerate(results_with_scores, 1):
            print(f"      {i}. Score: {score:.4f}")
            print(f"         Content: {doc.page_content[:100]}...")
            print(f"         Source: {doc.metadata.get('source', 'Unknown')}")
            
    except Exception as e:
        print(f"   ❌ Error in similarity search: {e}")
    
    # Step 7: Cleanup
    print("\n7️⃣ Cleanup:")
    try:
        # Clear the vector store
        if vector_store.clear_collection():
            print("   ✅ Vector store cleared successfully")
        else:
            print("   ❌ Failed to clear vector store")
    except Exception as e:
        print(f"   ❌ Error during cleanup: {e}")
    
    print("\n🎉 Example completed successfully!")
    print("\n💡 Next steps:")
    print("   - Try the web interface: streamlit run streamlit_app.py")
    print("   - Use the CLI: python cli_app.py")
    print("   - Upload your own documents")
    print("   - Customize the configuration in config.py")

if __name__ == "__main__":
    main()
