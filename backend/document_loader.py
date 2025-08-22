import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
    UnstructuredFileLoader
)
from langchain_core.documents import Document
from config import Config

class DocumentLoader:
    """Handles loading and processing various document types for RAG system."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load and chunk a PDF file."""
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
            return []
    
    def load_text(self, file_path: str) -> List[Document]:
        """Load and chunk a text file."""
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"Error loading text file {file_path}: {e}")
            return []
    
    def load_directory(self, directory_path: str, glob_pattern: str = "**/*") -> List[Document]:
        """Load all documents from a directory."""
        try:
            loader = DirectoryLoader(
                directory_path,
                glob=glob_pattern,
                loader_cls=UnstructuredFileLoader
            )
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"Error loading directory {directory_path}: {e}")
            return []
    
    def load_file(self, file_path: str) -> List[Document]:
        """Automatically detect file type and load accordingly."""
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return []
        
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self.load_pdf(file_path)
        elif file_extension in ['txt', 'md', 'py', 'js', 'html', 'css']:
            return self.load_text(file_path)
        else:
            try:
                # Try using unstructured loader for other file types
                loader = UnstructuredFileLoader(file_path)
                documents = loader.load()
                return self.text_splitter.split_documents(documents)
            except Exception as e:
                print(f"Unsupported file type or error loading {file_path}: {e}")
                return []
    
    def create_sample_documents(self) -> List[Document]:
        """Create sample documents for testing the RAG system."""
        sample_texts = [
            "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that work and react like humans.",
            "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
            "Deep Learning uses neural networks with multiple layers to model and understand complex patterns in data.",
            "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language.",
            "Retrieval-Augmented Generation (RAG) combines information retrieval with text generation to provide more accurate and contextual responses.",
            "Vector databases store high-dimensional vectors that represent text embeddings, enabling efficient similarity search.",
            "Embeddings are numerical representations of text that capture semantic meaning and can be used for similarity comparisons.",
            "Chunking is the process of breaking down large documents into smaller, manageable pieces for processing and storage."
        ]
        
        documents = []
        for i, text in enumerate(sample_texts):
            doc = Document(
                page_content=text,
                metadata={
                    "source": f"sample_doc_{i+1}",
                    "type": "sample",
                    "id": i+1
                }
            )
            documents.append(doc)
        
        return documents
