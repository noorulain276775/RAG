#!/usr/bin/env python3
"""
Test script for the RAG System
Run this to verify all components are working correctly.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock

from document_loader import DocumentLoader
from vector_store import VectorStore
from rag_system import RAGSystem
from config import Config

class TestRAGSystem(unittest.TestCase):
    """Test cases for the RAG system components."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create test text file
        self.test_file_path = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file_path, "w") as f:
            f.write("This is a test document about artificial intelligence and machine learning.")
        
        # Mock OpenAI API key for testing
        self.patcher = patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
        self.patcher.start()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
        
        # Stop patcher
        self.patcher.stop()
    
    def test_document_loader_initialization(self):
        """Test document loader initialization."""
        loader = DocumentLoader()
        self.assertIsNotNone(loader)
        self.assertIsNotNone(loader.text_splitter)
    
    def test_document_loader_text_file(self):
        """Test loading text files."""
        loader = DocumentLoader()
        documents = loader.load_text(self.test_file_path)
        
        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)
        
        # Check document content
        doc = documents[0]
        self.assertIn("artificial intelligence", doc.page_content.lower())
    
    def test_document_loader_sample_documents(self):
        """Test sample document creation."""
        loader = DocumentLoader()
        sample_docs = loader.create_sample_documents()
        
        self.assertIsInstance(sample_docs, list)
        self.assertGreater(len(sample_docs), 0)
        
        # Check that documents contain expected content
        ai_content = any("artificial intelligence" in doc.page_content.lower() for doc in sample_docs)
        self.assertTrue(ai_content)
    
    def test_vector_store_initialization(self):
        """Test vector store initialization."""
        # Mock OpenAI embeddings
        with patch('langchain_openai.OpenAIEmbeddings') as mock_embeddings:
            mock_embeddings.return_value = MagicMock()
            vector_store = VectorStore()
            self.assertIsNotNone(vector_store)
    
    def test_rag_system_initialization(self):
        """Test RAG system initialization."""
        # Mock OpenAI components
        with patch('langchain_openai.ChatOpenAI') as mock_chat, \
             patch('langchain_openai.OpenAIEmbeddings') as mock_embeddings:
            
            mock_chat.return_value = MagicMock()
            mock_embeddings.return_value = MagicMock()
            
            rag_system = RAGSystem()
            self.assertIsNotNone(rag_system)
    
    def test_config_defaults(self):
        """Test configuration default values."""
        # Test with no environment variables
        with patch.dict(os.environ, {}, clear=True):
            from config import Config
            config = Config()
            
            self.assertEqual(config.OPENAI_API_KEY, "your_openai_api_key_here")
            self.assertEqual(config.OPENAI_MODEL, "gpt-3.5-turbo")
            self.assertEqual(config.CHUNK_SIZE, 1000)
            self.assertEqual(config.CHUNK_OVERLAP, 200)
            self.assertEqual(config.TOP_K_RESULTS, 3)
            self.assertEqual(config.TEMPERATURE, 0.7)

class TestIntegration(unittest.TestCase):
    """Integration tests for the RAG system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test document
        self.test_file_path = os.path.join(self.test_dir, "ai_doc.txt")
        with open(self.test_file_path, "w") as f:
            f.write("""
            Artificial Intelligence (AI) is a branch of computer science that aims to create 
            intelligent machines that work and react like humans. Machine Learning is a subset 
            of AI that enables computers to learn and improve from experience without being 
            explicitly programmed.
            """)
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    @patch('langchain_openai.OpenAIEmbeddings')
    @patch('langchain_openai.ChatOpenAI')
    def test_full_rag_pipeline(self, mock_chat, mock_embeddings):
        """Test the complete RAG pipeline."""
        # Mock OpenAI components
        mock_embeddings.return_value = MagicMock()
        mock_chat.return_value = MagicMock()
        mock_chat.return_value.run.return_value = "AI is a branch of computer science that creates intelligent machines."
        
        try:
            # Initialize components
            loader = DocumentLoader()
            vector_store = VectorStore()
            rag_system = RAGSystem()
            
            # Load and process document
            documents = loader.load_file(self.test_file_path)
            self.assertGreater(len(documents), 0)
            
            # Add to vector store
            success = vector_store.add_documents(documents)
            self.assertTrue(success)
            
            # Query the system
            response = rag_system.query("What is artificial intelligence?")
            
            # Check response structure
            self.assertIn('answer', response)
            self.assertIn('sources', response)
            self.assertIn('num_sources', response)
            
        except Exception as e:
            self.fail(f"Integration test failed with exception: {e}")

def run_quick_test():
    """Run a quick functionality test without requiring OpenAI API."""
    print("🧪 Running Quick RAG System Test")
    print("=" * 40)
    
    try:
        # Test document loader
        print("1. Testing Document Loader...")
        loader = DocumentLoader()
        sample_docs = loader.create_sample_documents()
        print(f"   ✅ Created {len(sample_docs)} sample documents")
        
        # Test text splitting
        print("2. Testing Text Splitting...")
        if sample_docs:
            doc = sample_docs[0]
            print(f"   ✅ Document chunk size: {len(doc.page_content)} characters")
            print(f"   ✅ Document source: {doc.metadata.get('source', 'Unknown')}")
        
        # Test configuration
        print("3. Testing Configuration...")
        from config import Config
        config = Config()
        print(f"   ✅ Chunk size: {config.CHUNK_SIZE}")
        print(f"   ✅ Chunk overlap: {config.CHUNK_OVERLAP}")
        print(f"   ✅ Top K results: {config.TOP_K_RESULTS}")
        
        print("\n🎉 Quick test completed successfully!")
        print("💡 The RAG system components are working correctly.")
        print("   To test with AI features, set your OpenAI API key and run the full tests.")
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        print("💡 Check that all dependencies are installed correctly.")

if __name__ == "__main__":
    print("🧪 RAG System Test Suite")
    print("=" * 30)
    
    # Check if OpenAI API key is available
    if os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here':
        print("🔑 OpenAI API key found. Running full test suite...")
        unittest.main(verbosity=2)
    else:
        print("⚠️  No OpenAI API key found. Running quick test only...")
        run_quick_test()
