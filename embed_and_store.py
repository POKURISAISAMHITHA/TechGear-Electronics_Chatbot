"""
RAG System Setup: Load product info, create embeddings, and store in ChromaDB
Uses LangChain, ChromaDB, and Google Generative AI Embeddings
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables from .env file
load_dotenv()

# Get the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


def load_and_embed_documents():
    """
    Load product info from text file, split into chunks,
    create embeddings, and store in ChromaDB
    """
    
    print("=" * 60)
    print("Starting RAG Pipeline Setup")
    print("=" * 60)
    
    # Step 1: Load the document using TextLoader
    print("\n[Step 1] Loading document from product_info.txt...")
    loader = TextLoader("product_info.txt")
    documents = loader.load()
    print(f"✓ Document loaded successfully")
    print(f"  - Total documents: {len(documents)}")
    print(f"  - Document size: {len(documents[0].page_content)} characters")
    
    # Step 2: Split text into chunks
    print("\n[Step 2] Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✓ Text split successfully")
    print(f"  - Total chunks: {len(chunks)}")
    print(f"  - Chunk size: 500 characters (with 50 character overlap)")
    
    # Display sample chunks
    print("\n  Sample chunks:")
    for i, chunk in enumerate(chunks[:3], 1):
        preview = chunk.page_content[:100].replace('\n', ' ')
        print(f"    Chunk {i}: {preview}...")
    
    # Step 3: Create embeddings using Google Generative AI
    print("\n[Step 3] Creating embeddings using Google Generative AI...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
    print("✓ Embeddings model initialized")
    print("  - Model: models/embedding-001")
    
    # Step 4: Store embeddings in ChromaDB (with persistence)
    print("\n[Step 4] Storing embeddings in ChromaDB...")
    
    # Define persist directory
    persist_directory = "chroma_db"
    
    # Create Chroma vectorstore with persistence
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="product_info"
    )
    
    print(f"✓ Embeddings stored in ChromaDB")
    print(f"  - Persist directory: {persist_directory}")
    print(f"  - Collection name: product_info")
    print(f"  - Number of vectors: {len(chunks)}")
    
    # Verify persistence
    vectorstore.persist()
    print("✓ Database persisted to disk")
    
    print("\n" + "=" * 60)
    print("RAG Pipeline Setup Complete!")
    print("=" * 60)
    
    return vectorstore, chunks


def test_retrieval(vectorstore):
    """
    Test the retrieval system with sample queries
    """
    print("\n" + "=" * 60)
    print("Testing Retrieval System")
    print("=" * 60)
    
    # Sample queries
    test_queries = [
        "What is the price of SmartWatch Pro X?",
        "What are the warranty options?",
        "What is the return policy?",
        "What features does the Power Bank have?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        
        # Retrieve relevant documents
        results = vectorstore.similarity_search(query, k=2)
        
        for i, result in enumerate(results, 1):
            print(f"  Result {i}:")
            print(f"  {result.page_content[:150]}...")
            print()


def load_existing_vectorstore():
    """
    Load an existing ChromaDB vectorstore from disk
    """
    print("\nLoading existing vectorstore from disk...")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
    
    persist_directory = "chroma_db"
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="product_info"
    )
    
    print(f"✓ Vectorstore loaded from {persist_directory}")
    return vectorstore


if __name__ == "__main__":
    try:
        # Create and setup the RAG pipeline
        vectorstore, chunks = load_and_embed_documents()
        
        # Test the retrieval system
        test_retrieval(vectorstore)
        
        print("\n" + "=" * 60)
        print("Setup completed successfully!")
        print("ChromaDB is ready for use in your chatbot.")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure 'product_info.txt' exists in the current directory")
    except Exception as e:
        print(f"Error during setup: {e}")
        raise
