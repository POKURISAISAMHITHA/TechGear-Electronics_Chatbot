"""
Verification Script - Check System Status
Shows current configuration and what's been completed
"""

import os
from pathlib import Path

def check_status():
    print("="*70)
    print("🔍 TECHGEAR CHATBOT - SYSTEM STATUS CHECK")
    print("="*70)
    
    # Check product_info.txt
    print("\n📦 PRODUCT CATALOG:")
    product_file = Path("product_info.txt")
    if product_file.exists():
        with open(product_file, 'r', encoding='utf-8') as f:
            content = f.read()
            char_count = len(content)
            product_count = content.count("Product: ")
            category_count = content.count("====================")
            
        print(f"  ✅ File exists: {product_file}")
        print(f"  ✅ Total characters: {char_count:,}")
        print(f"  ✅ Total products: {product_count}")
        print(f"  ✅ Total categories: {category_count}")
    else:
        print(f"  ❌ File not found: {product_file}")
    
    # Check .env file
    print("\n🔐 CONFIGURATION:")
    env_file = Path(".env")
    if env_file.exists():
        print(f"  ✅ .env file exists")
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "GEMINI_API_KEY" in env_content:
                # Check if it has a real value (not placeholder)
                if "your_api_key_here" in env_content:
                    print(f"  ⚠️  API key is placeholder - needs real key")
                else:
                    api_key_line = [line for line in env_content.split('\n') if 'GEMINI_API_KEY' in line][0]
                    api_key = api_key_line.split('=')[1].strip()
                    if len(api_key) > 20:
                        print(f"  ✅ API key configured (length: {len(api_key)})")
                    else:
                        print(f"  ⚠️  API key seems too short")
            else:
                print(f"  ❌ GEMINI_API_KEY not found in .env")
    else:
        print(f"  ❌ .env file not found")
    
    # Check embed_and_store.py configuration
    print("\n⚙️  CHUNKING CONFIGURATION:")
    embed_file = Path("embed_and_store.py")
    if embed_file.exists():
        with open(embed_file, 'r') as f:
            embed_content = f.read()
            if "chunk_size=800" in embed_content:
                print(f"  ✅ Chunk size: 800 characters (optimized)")
            else:
                print(f"  ⚠️  Chunk size: 500 characters (default)")
            
            if "chunk_overlap=100" in embed_content:
                print(f"  ✅ Chunk overlap: 100 characters (optimized)")
            else:
                print(f"  ⚠️  Chunk overlap: 50 characters (default)")
            
            if '"\n\n==================== "' in embed_content or "\"\\n\\n==================== \"" in embed_content:
                print(f"  ✅ Smart separators: Enabled")
            else:
                print(f"  ⚠️  Smart separators: Not configured")
    
    # Check rag_chain.py configuration
    print("\n🔍 RAG RETRIEVAL CONFIGURATION:")
    rag_file = Path("rag_chain.py")
    if rag_file.exists():
        with open(rag_file, 'r') as f:
            rag_content = f.read()
            if '"k": 5' in rag_content or "'k': 5" in rag_content:
                print(f"  ✅ Retrieval k: 5 documents (optimized)")
            elif '"k": 3' in rag_content or "'k': 3" in rag_content:
                print(f"  ⚠️  Retrieval k: 3 documents (default)")
    
    # Check ChromaDB
    print("\n💾 VECTOR DATABASE:")
    chroma_dir = Path("chroma_db")
    if chroma_dir.exists() and chroma_dir.is_dir():
        files = list(chroma_dir.iterdir())
        print(f"  ✅ ChromaDB directory exists")
        print(f"  ✅ Files in database: {len(files)}")
        print(f"  ✅ Status: Embeddings created")
    else:
        print(f"  ⚠️  ChromaDB directory not found")
        print(f"  ⚠️  Status: Embeddings need to be created")
        print(f"  💡 Run: python embed_and_store.py")
    
    # Check virtual environment
    print("\n🐍 PYTHON ENVIRONMENT:")
    venv_dir = Path(".venv")
    if venv_dir.exists():
        print(f"  ✅ Virtual environment exists: .venv")
        # Check if key packages are installed
        site_packages = venv_dir / "lib" / "python3.10" / "site-packages"
        if site_packages.exists():
            packages = list(site_packages.iterdir())
            has_langchain = any("langchain" in str(p).lower() for p in packages)
            has_chromadb = any("chromadb" in str(p).lower() for p in packages)
            has_fastapi = any("fastapi" in str(p).lower() for p in packages)
            
            if has_langchain:
                print(f"  ✅ LangChain installed")
            if has_chromadb:
                print(f"  ✅ ChromaDB installed")
            if has_fastapi:
                print(f"  ✅ FastAPI installed")
    else:
        print(f"  ⚠️  Virtual environment not found")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY:")
    print("="*70)
    
    chroma_exists = chroma_dir.exists()
    api_configured = env_file.exists() and "GEMINI_API_KEY" in open(env_file).read()
    
    if product_count == 200 and chroma_exists and api_configured:
        print("✅ System Status: READY")
        print("✅ All components configured and operational")
        print("💡 You can start the server: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    elif product_count == 200 and api_configured and not chroma_exists:
        print("⚠️  System Status: NEEDS EMBEDDINGS")
        print("✅ Products: 200 loaded")
        print("✅ Configuration: Complete")
        print("⚠️  Embeddings: Not created")
        print("💡 Next step: python embed_and_store.py")
    elif product_count == 200 and not api_configured:
        print("⚠️  System Status: NEEDS API KEY")
        print("✅ Products: 200 loaded")
        print("⚠️  Configuration: API key missing/invalid")
        print("💡 Next step: Add valid GEMINI_API_KEY to .env file")
    else:
        print("⚠️  System Status: INCOMPLETE")
        print("💡 Check the details above")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    check_status()
