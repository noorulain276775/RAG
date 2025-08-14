#!/usr/bin/env python3
"""
Setup script for the RAG System
Automates the installation and initial configuration process.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip not found. Please install pip first.")
        return False
    
    try:
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file with configuration template."""
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    print("\n🔧 Creating .env configuration file...")
    
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# RAG Configuration
TOP_K_RESULTS=3
TEMPERATURE=0.7
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("💡 Please edit .env and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating project directories...")
    
    directories = [
        "chroma_db",
        "documents",
        "logs"
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"   ✅ Created {directory}/")
        except Exception as e:
            print(f"   ⚠️  Could not create {directory}/: {e}")
    
    return True

def run_quick_test():
    """Run a quick test to verify installation."""
    print("\n🧪 Running quick installation test...")
    
    try:
        # Test imports
        import langchain
        import streamlit
        import chromadb
        print("   ✅ All core packages imported successfully")
        
        # Test configuration
        from config import Config
        config = Config()
        print(f"   ✅ Configuration loaded: chunk_size={config.CHUNK_SIZE}")
        
        print("✅ Installation test passed!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def show_next_steps():
    """Display next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Test the system: python test_rag.py")
    print("3. Run the web interface: streamlit run streamlit_app.py")
    print("4. Use the CLI: python cli_app.py")
    print("5. Try the example: python example_usage.py")
    
    print("\n🔑 Getting OpenAI API Key:")
    print("   - Visit: https://platform.openai.com/")
    print("   - Sign up or sign in")
    print("   - Go to API Keys section")
    print("   - Create a new API key")
    print("   - Copy the key to your .env file")
    
    print("\n💡 Quick start commands:")
    print("   python test_rag.py          # Test the system")
    print("   streamlit run streamlit_app.py  # Web interface")
    print("   python cli_app.py --sample  # CLI with sample data")

def main():
    """Main setup function."""
    print("🚀 RAG System Setup")
    print("=" * 30)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Create configuration
    if not create_env_file():
        print("\n❌ Setup failed. Could not create configuration file.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Test installation
    if not run_quick_test():
        print("\n⚠️  Setup completed with warnings. Some features may not work.")
    else:
        print("\n✅ All tests passed!")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
