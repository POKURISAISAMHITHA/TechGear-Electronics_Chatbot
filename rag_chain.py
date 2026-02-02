"""
RAG Chain Implementation: Load ChromaDB, create retriever, and build RAG chain with Gemini
Uses LangChain, ChromaDB, and Google Generative AI (Gemini)
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


def format_docs(docs):
    """Format retrieved documents for the prompt"""
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain():
    """
    Create a complete RAG chain:
    1. Load existing ChromaDB vector store
    2. Create a retriever (top k = 3)
    3. Initialize Gemini model
    4. Create RetrievalQA chain
    5. Return the final RAG chain
    """
    
    print("=" * 70)
    print("Building RAG Chain with Gemini")
    print("=" * 70)
    
    # Step 1: Load existing ChromaDB vector store
    print("\n[Step 1] Loading ChromaDB vector store...")
    persist_directory = "chroma_db"
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="product_info"
    )
    print(f"✓ ChromaDB loaded successfully")
    print(f"  - Persist directory: {persist_directory}")
    print(f"  - Collection: product_info")
    
    # Step 2: Create retriever - optimized for speed and accuracy
    print("\n[Step 2] Creating retriever...")
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4  # Optimal balance: 4 chunks * 600 chars = 2400 chars context
        }
    )
    print(f"✓ Retriever created")
    print(f"  - Top K: 4 documents (optimized)")
    print(f"  - Search type: similarity")
    print(f"  - Total context: ~2400 characters")
    
    # Step 3: Initialize Gemini model
    print("\n[Step 3] Initializing Gemini model...")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
    except:
        # Fallback to a different model name
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
    print(f"✓ Gemini model initialized")
    print(f"  - Model: gemini-1.5-flash-latest")
    print(f"  - Temperature: 0.7")
    
    # Step 4: Create custom prompt template
    print("\n[Step 4] Creating prompt template...")
    prompt_template = """You are a Retrieval-Augmented chatbot for TechGear Electronics customer support.

INSTRUCTIONS (VERY IMPORTANT):
- Answer ONLY what the user asked
- DO NOT repeat the full product description
- DO NOT include unrelated details
- Extract only the specific information needed
- Keep the answer short and precise
- If the question is about price, return ONLY the price
- If the question is about warranty, return ONLY warranty details

ACRONYM HANDLING:
- COD = Cash on Delivery
- EMI = Equated Monthly Installments
- UPI = Unified Payments Interface
- If user asks "is cod available?" they mean "is Cash on Delivery available?"
- If user asks about "emi" they mean EMI payment options
- Expand acronyms when searching context

BRAND-SPECIFIC QUERIES:
- If the user asks about a specific brand (e.g., "AirPods", "MacBook", "iPhone", "Samsung Galaxy"):
  * Check if that EXACT brand/model exists in the context
  * If NOT found, say: "We don't sell [brand name], but we have similar products like [list alternatives]"
  * DO NOT list random unrelated products
- Example: "Do you sell AirPods?" → If no AirPods in context → "We don't sell AirPods, but we have Wireless Earbuds Elite and Earbuds Pro Max"

PRODUCT NAME MATCHING:
- If the user asks about a product with a slightly different name or size (e.g., "Pro 15" vs "Pro 14"), 
  find the CLOSEST matching product in the context
- If you find a very similar product (same brand/model but different size), answer about that product
  and clarify: "We have the [actual product name] at [price/info]"
- Only say "Information not available" if NO similar product exists at all

FORMAT RULES:
- Do NOT include headings like "Product:"
- DO NOT list all features unless explicitly asked
- Answer in 1–2 sentences maximum

Context:
{context}

Question: {question}

Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    print(f"✓ Prompt template created")
    
    # Step 5: Create RAG chain using LCEL (LangChain Expression Language)
    print("\n[Step 5] Creating RAG chain...")
    
    # Define the chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )
    
    print(f"✓ RAG chain created")
    print(f"  - Chain type: Retrieval-Augmented Generation")
    print(f"  - Returns formatted response: True")
    
    print("\n" + "=" * 70)
    print("RAG Chain Ready!")
    print("=" * 70)
    
    return rag_chain


def query_rag_chain(rag_chain, retriever, query):
    """
    Query the RAG chain and return the response with source documents
    
    Args:
        rag_chain: The RAG chain
        retriever: The retriever for getting source documents
        query: User's question
    
    Returns:
        Dictionary with answer and source documents
    """
    print(f"\n{'=' * 70}")
    print(f"Query: {query}")
    print(f"{'=' * 70}")
    
    # Get response from RAG chain
    answer = rag_chain.invoke(query)
    
    # Get source documents
    source_docs = retriever.invoke(query)
    
    # Display answer
    print(f"\nAnswer:\n{answer}")
    
    # Display source documents
    if source_docs:
        print(f"\nSource Documents:")
        for i, doc in enumerate(source_docs, 1):
            print(f"\n  Document {i}:")
            print(f"  {doc.page_content[:150]}...")
    
    return {"answer": answer, "source_documents": source_docs}


def main(test_queries=True):
    """Main function to demonstrate RAG chain usage"""
    
    try:
        # Create the RAG chain
        rag_chain = create_rag_chain()
        
        if not test_queries:
            return rag_chain
        
        # Sample queries to test the RAG chain
        test_query_list = [
            "What is the price of SmartWatch Pro X?",
            "What warranty options are available?",
            "What is your return policy?",
            "Tell me about the Power Bank Ultra",
            "What are the features of Wireless Earbuds Elite?"
        ]
        
        # Recreate retriever for source document retrieval
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
        
        # Query the RAG chain
        for query in test_query_list:
            try:
                response = query_rag_chain(rag_chain, retriever, query)
                print("\n" + "-" * 70)
            except Exception as e:
                print(f"Error querying: {e}")
                print(f"Note: Make sure your GEMINI_API_KEY in .env is valid")
                break
        
        print("\n" + "=" * 70)
        print("RAG Chain Setup Complete!")
        print("=" * 70)
        
        # Return the chain for programmatic use
        return rag_chain
        
    except FileNotFoundError:
        print("Error: ChromaDB not found. Please run embed_and_store.py first.")
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    # Set test_queries=False to skip testing (useful if API key is invalid)
    # Set test_queries=True to run sample queries
    rag_chain = main(test_queries=False)
