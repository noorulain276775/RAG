#!/usr/bin/env python3
"""
Command Line Interface for the RAG System
"""

import argparse
import sys
import os
from typing import List

from document_loader import DocumentLoader
from vector_store import VectorStore
from rag_system import RAGSystem
from config import Config

class RAGCLI:
    """Command Line Interface for the RAG system."""
    
    def __init__(self):
        self.rag_system = None
        self.vector_store = None
        self.document_loader = None
    
    def initialize_system(self):
        """Initialize the RAG system components."""
        try:
            print("🚀 Initializing RAG system...")
            self.document_loader = DocumentLoader()
            self.vector_store = VectorStore()
            self.rag_system = RAGSystem()
            print("✅ RAG system initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Error initializing RAG system: {e}")
            print("💡 Please check your OpenAI API key in the configuration.")
            return False
    
    def interactive_mode(self):
        """Run the CLI in interactive mode."""
        if not self.rag_system:
            if not self.initialize_system():
                return
        
        print("\n🤖 Welcome to the RAG CLI!")
        print("Type 'help' for available commands, 'quit' to exit.")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if user_input.lower() == 'clear':
                    self.clear_knowledge_base()
                    continue
                
                # Process as a question
                print("🤔 Thinking...")
                response = self.rag_system.query(user_input)
                
                print(f"\n🤖 Assistant: {response['answer']}")
                
                if response.get('sources'):
                    print(f"\n📚 Sources ({response['num_sources']}):")
                    for i, source in enumerate(response['sources'], 1):
                        print(f"  {i}. {source['content'][:100]}...")
                        print(f"     Source: {source.get('metadata', {}).get('source', 'Unknown')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def query_mode(self, question: str):
        """Run a single query and exit."""
        if not self.rag_system:
            if not self.initialize_system():
                return
        
        print(f"🤔 Question: {question}")
        print("🤔 Thinking...")
        
        response = self.rag_system.query(question)
        
        print(f"\n🤖 Answer: {response['answer']}")
        
        if response.get('sources'):
            print(f"\n📚 Sources ({response['num_sources']}):")
            for i, source in enumerate(response['sources'], 1):
                print(f"  {i}. {source['content'][:100]}...")
                print(f"     Source: {source.get('metadata', {}).get('source', 'Unknown')}")
    
    def load_documents(self, file_paths: List[str]):
        """Load documents from file paths."""
        if not self.document_loader:
            if not self.initialize_system():
                return
        
        total_docs = 0
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"⚠️  File not found: {file_path}")
                continue
            
            print(f"📚 Processing: {file_path}")
            try:
                documents = self.document_loader.load_file(file_path)
                
                if documents:
                    success = self.vector_store.add_documents(documents)
                    if success:
                        total_docs += len(documents)
                        print(f"✅ Processed {file_path}: {len(documents)} chunks")
                    else:
                        print(f"❌ Failed to add {file_path} to vector store")
                else:
                    print(f"⚠️  No content extracted from {file_path}")
                    
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
        
        if total_docs > 0:
            print(f"\n🎉 Successfully processed {total_docs} document chunks!")
    
    def load_sample_documents(self):
        """Load sample documents for testing."""
        if not self.document_loader:
            if not self.initialize_system():
                return
        
        print("📚 Loading sample documents...")
        try:
            sample_docs = self.document_loader.create_sample_documents()
            
            if sample_docs:
                success = self.vector_store.add_documents(sample_docs)
                if success:
                    print(f"✅ Loaded {len(sample_docs)} sample document chunks!")
                    print("💡 You can now ask questions about AI, Machine Learning, and RAG systems!")
                else:
                    print("❌ Failed to add sample documents to vector store")
            else:
                print("❌ Failed to create sample documents")
                
        except Exception as e:
            print(f"❌ Error loading sample documents: {e}")
    
    def show_stats(self):
        """Show system statistics."""
        if not self.rag_system:
            print("❌ RAG system not initialized. Use 'init' first.")
            return
        
        try:
            config = self.rag_system.get_system_info()
            print("\n📊 System Statistics:")
            print(f"  Model: {config['model']}")
            print(f"  Temperature: {config['temperature']}")
            print(f"  Chunk Size: {config['chunk_size']}")
            print(f"  Chunk Overlap: {config['chunk_overlap']}")
            print(f"  Top K Results: {config['top_k_results']}")
            
            if 'vector_store_stats' in config:
                stats = config['vector_store_stats']
                print(f"  Total Documents: {stats.get('total_documents', 'Unknown')}")
                print(f"  Persist Directory: {stats.get('persist_directory', 'Unknown')}")
                print(f"  Embedding Model: {stats.get('embedding_model', 'Unknown')}")
                
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
    
    def clear_knowledge_base(self):
        """Clear the knowledge base."""
        if not self.vector_store:
            print("❌ Vector store not initialized.")
            return
        
        try:
            if self.vector_store.clear_collection():
                print("✅ Knowledge base cleared!")
            else:
                print("❌ Failed to clear knowledge base")
        except Exception as e:
            print(f"❌ Error clearing knowledge base: {e}")
    
    def show_help(self):
        """Show available commands."""
        print("\n📖 Available Commands:")
        print("  help                    - Show this help message")
        print("  stats                   - Show system statistics")
        print("  clear                   - Clear the knowledge base")
        print("  quit/exit/q             - Exit the CLI")
        print("  <any text>              - Ask a question")
        print("\n💡 Just type your question and press Enter!")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RAG System Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_app.py                    # Interactive mode
  python cli_app.py -q "What is AI?"   # Single query mode
  python cli_app.py -f doc1.pdf doc2.txt  # Load documents
  python cli_app.py --sample           # Load sample documents
        """
    )
    
    parser.add_argument(
        '-q', '--query',
        type=str,
        help='Run a single query and exit'
    )
    
    parser.add_argument(
        '-f', '--files',
        nargs='+',
        help='Load documents from specified file paths'
    )
    
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Load sample documents for testing'
    )
    
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize the system and show stats'
    )
    
    args = parser.parse_args()
    
    cli = RAGCLI()
    
    try:
        if args.init:
            if cli.initialize_system():
                cli.show_stats()
            return
        
        if args.files:
            cli.load_documents(args.files)
            return
        
        if args.sample:
            cli.load_sample_documents()
            return
        
        if args.query:
            cli.query_mode(args.query)
            return
        
        # Default to interactive mode
        cli.interactive_mode()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
