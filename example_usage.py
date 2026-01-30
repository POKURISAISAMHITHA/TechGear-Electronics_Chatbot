"""
Example: How to use the RAG chain programmatically
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from rag_chain import create_rag_chain

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def example_usage():
    """
    Demonstrates how to use the RAG chain for customer support queries
    """
    
    print("=" * 70)
    print("RAG Chatbot Example Usage")
    print("=" * 70)
    
    # Step 1: Create the RAG chain
    print("\nInitializing RAG chain...")
    rag_chain = create_rag_chain()
    
    # Step 2: Load retriever for source documents
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings,
        collection_name="product_info"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Step 3: Define example queries
    queries = [
        "What is the price of SmartWatch Pro X?",
        "Do you offer warranty?",
        "What is the return policy?",
    ]
    
    print("\n" + "=" * 70)
    print("Running Example Queries")
    print("=" * 70)
    
    for query in queries:
        print(f"\n{'─' * 70}")
        print(f"Customer: {query}")
        print(f"{'─' * 70}")
        
        try:
            # Get answer from RAG chain
            answer = rag_chain.invoke(query)
            print(f"Assistant: {answer}")
            
            # Get source documents
            docs = retriever.invoke(query)
            print(f"\n[Retrieved {len(docs)} source document(s)]")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("\nTip: Ensure your GEMINI_API_KEY in .env is valid and active.")
    
    print("\n" + "=" * 70)
    print("Example Complete!")
    print("=" * 70)


if __name__ == "__main__":
    example_usage()
