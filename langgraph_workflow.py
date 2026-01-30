"""
LangGraph Workflow: Intelligent Customer Support with Classification and Routing
- StateGraph with multi-node workflow
- Query classifier using Gemini (with fallback)
- RAG responder for known queries
- Escalation for unknown queries
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Try to import RAG chain (optional)
try:
    from rag_chain import create_rag_chain
    RAG_AVAILABLE = True
except Exception as e:
    print(f"Warning: RAG chain not available: {e}")
    RAG_AVAILABLE = False


# ============================================================================
# STATE DEFINITION
# ============================================================================

class SupportState(TypedDict):
    """State for the customer support workflow"""
    user_query: str
    category: str  # products, returns, general, unknown
    response: str


# ============================================================================
# NODE 1: CLASSIFIER
# ============================================================================

def classifier_node(state: SupportState) -> SupportState:
    """
    Classify user query into categories using Gemini (with fallback)
    Categories: products, returns, general, unknown
    """
    
    print("\n" + "=" * 70)
    print("NODE: CLASSIFIER")
    print("=" * 70)
    print(f"Query: {state['user_query']}")
    
    # Try Gemini classification first
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=GEMINI_API_KEY,
            temperature=0.3
        )
        
        classification_prompt = """You are a customer support classifier. Classify the following query into ONE category:

Categories:
- products: Questions about product features, specifications, pricing, availability, what products we sell
- returns: Questions about return policy, refunds, exchanges
- general: General questions about support hours, contact info, company info
- unknown: Anything that doesn't fit above categories

Query: {query}

Respond with ONLY the category name (products, returns, general, or unknown). No other text."""
        
        prompt = PromptTemplate(
            template=classification_prompt,
            input_variables=["query"]
        )
        
        classification_chain = prompt | llm
        category = classification_chain.invoke({"query": state["user_query"]}).content.strip().lower()
        
        valid_categories = ["products", "returns", "general", "unknown"]
        if category not in valid_categories:
            category = "unknown"
        
        print(f"Classified as: {category}")
        
        return {
            "user_query": state["user_query"],
            "category": category,
            "response": state.get("response", "")
        }
    
    except Exception as e:
        print(f"Gemini classification failed: {e}")
        print(f"Using keyword-based fallback classification...")
        
        # Fallback to keyword-based classification
        query_lower = state["user_query"].lower().strip()
        
        # Greetings and acknowledgments - classify as general
        greetings = ["hi", "hello", "hey", "greetings", "ok", "okay", "k", "thanks", "thank you", "thankyou", "got it", "understood"]
        if query_lower in greetings or any(query_lower.startswith(g + " ") for g in greetings):
            category = "general"
        elif any(word in query_lower for word in ["price", "cost", "feature", "product", "smartwatch", "earbuds", "power bank", "sell", "what do you", "which", "list"]):
            category = "products"
        elif any(word in query_lower for word in ["return", "refund", "exchange", "policy"]):
            category = "returns"
        elif any(word in query_lower for word in ["support", "hours", "contact", "help", "email", "question", "questions"]):
            category = "general"
        else:
            category = "unknown"
        
        print(f"Fallback classified as: {category}")
        
        return {
            "user_query": state["user_query"],
            "category": category,
            "response": state.get("response", "")
        }


# ============================================================================
# NODE 2: RAG RESPONDER
# ============================================================================

def rag_responder_node(state: SupportState) -> SupportState:
    """
    Use RAG chain or concise responses to generate answers
    """
    
    print("\n" + "=" * 70)
    print("NODE: RAG RESPONDER")
    print("=" * 70)
    print(f"Query: {state['user_query']}")
    print(f"Category: {state['category']}")
    
    # Check if asking for product list
    query_lower = state["user_query"].lower()
    product_triggers = [
        "what products",
        "what do you sell",
        "products do you sell",
        "list of products",
        "which products",
        "sell"
    ]
    
    if any(trigger in query_lower for trigger in product_triggers) and "products" in state["category"]:
        products = "SmartWatch Pro X, Wireless Earbuds Elite, Power Bank Ultra"
        print(f"Product list response: {products}")
        return {
            "user_query": state["user_query"],
            "category": state["category"],
            "response": products
        }
    
    # Try RAG chain
    if RAG_AVAILABLE:
        try:
            rag_chain = create_rag_chain()
            response = rag_chain.invoke(state["user_query"])
            print(f"Response: {response[:100]}...")
            
            return {
                "user_query": state["user_query"],
                "category": state["category"],
                "response": response
            }
        except Exception as e:
            print(f"RAG error: {e}")
            print(f"Using fallback response...")
    
    # Fallback to concise responses
    response = get_concise_response(state["user_query"])
    
    return {
        "user_query": state["user_query"],
        "category": state["category"],
        "response": response
    }


def get_concise_response(query: str) -> str:
    """
    Generate CONCISE, SPECIFIC responses - answer ONLY what was asked
    For YES/NO questions, answer YES or NO first, then provide details if needed
    Handles greetings, acknowledgments, and product detail requests
    """
    query_lower = query.lower().strip()
    
    # ========== GREETING MESSAGES ==========
    greeting_responses = {
        "hi": "Hi! How can I help you today?",
        "hello": "Hello! What would you like to know?",
        "hey": "Hey! How can I assist you?",
        "greetings": "Hello! What can I help you with?",
    }
    
    for greeting, response in greeting_responses.items():
        if query_lower == greeting or query_lower.startswith(greeting + " "):
            return response
    
    # ========== ACKNOWLEDGMENT MESSAGES ==========
    acknowledgment_responses = {
        "ok": "Thank you! Hope my response was helpful. Feel free to ask if you have more questions!",
        "okay": "Thank you! Hope my response was helpful. Feel free to ask if you have more questions!",
        "k": "Thank you! Hope my response was helpful. Feel free to ask if you have more questions!",
        "thanks": "You're welcome! Happy to help. Anything else?",
        "thank you": "You're welcome! Happy to help. Anything else?",
        "thankyou": "You're welcome! Happy to help. Anything else?",
        "got it": "Great! Let me know if you need anything else.",
        "understood": "Perfect! Feel free to ask any other questions.",
    }
    
    for ack, response in acknowledgment_responses.items():
        if query_lower == ack or query_lower.startswith(ack + " "):
            return response
    
    # ========== PRODUCT DETAIL QUERIES ==========
    # Pattern: "I have questions on this <product>" or "Tell me about <product>"
    product_detail_triggers = [
        ("smartwatch", "SmartWatch Pro X: Price ₹15,999 | Heart rate monitoring, GPS tracking, 7-day battery life, water resistant (50m) | Standard warranty: 1 year, Extended: 2 years (₹1,999)"),
        ("earbuds", "Wireless Earbuds Elite: Price ₹7,999 | Active noise cancellation, premium sound, 20-hour battery, water resistant | Standard warranty: 1 year, Extended: 2 years (₹1,999)"),
        ("power bank", "Power Bank Ultra: Price ₹3,499 | 30,000mAh capacity, dual USB ports, fast charging support, compact design | Standard warranty: 1 year, Extended: 2 years (₹1,999)"),
    ]
    
    # Check if user is asking for product details
    detail_triggers = ["question", "questions", "tell me", "details", "about", "info", "information", "full details"]
    
    if any(trigger in query_lower for trigger in detail_triggers):
        for product_name, product_details in product_detail_triggers:
            if product_name in query_lower:
                return product_details
    
    # ========== YES/NO DETECTION ==========
    # Check if query is a YES/NO question
    is_yes_no_question = query.strip().endswith("?") and any(word in query_lower for word in ["can i", "can you", "do you", "does", "is", "are", "will", "have", "has", "could"])
    
    # ========== PRODUCT LISTING QUERIES ==========
    if any(word in query_lower for word in ["sell", "product", "products", "catalogue", "catalog", "available", "offer"]):
        if "list" in query_lower or "what" in query_lower or "which" in query_lower or "do you" in query_lower:
            return "SmartWatch Pro X, Wireless Earbuds Elite, Power Bank Ultra"
    
    # ========== YES/NO RETURN WINDOW QUERIES ==========
    if ("return" in query_lower or "refund" in query_lower) and ("30" in query_lower or "days" in query_lower or "can i" in query_lower or "can you" in query_lower):
        if is_yes_no_question:
            if "30" in query_lower:
                return "No. The return window is 7 days, not 30 days."
            elif "7" in query_lower:
                return "Yes. We offer a 7-day return window."
            else:
                return "Yes. We offer a 7-day return window for returns and refunds."
    
    # ========== YES/NO WARRANTY QUERIES ==========
    if "warranty" in query_lower and is_yes_no_question:
        if "extended" in query_lower or "2" in query_lower:
            return "Yes. Extended warranty (2 years) costs ₹1,999."
        return "Yes. Standard warranty is 1 year. Extended warranty (2 years) available for ₹1,999."
    
    # ========== YES/NO FEATURE QUERIES ==========
    if ("feature" in query_lower or "have" in query_lower or "support" in query_lower or "include" in query_lower) and is_yes_no_question:
        if "smartwatch" in query_lower:
            if "heart rate" in query_lower or "heart" in query_lower:
                return "Yes. SmartWatch Pro X has heart rate monitoring."
            elif "gps" in query_lower:
                return "Yes. SmartWatch Pro X has GPS tracking."
            elif "water" in query_lower or "waterproof" in query_lower:
                return "Yes. Water resistant up to 50m."
        elif "earbuds" in query_lower or "earbud" in query_lower:
            if "noise" in query_lower or "anc" in query_lower:
                return "Yes. Wireless Earbuds Elite have active noise cancellation."
        elif "power bank" in query_lower or "powerbank" in query_lower:
            if "fast" in query_lower or "charging" in query_lower:
                return "Yes. Power Bank Ultra supports fast charging."
    
    # ========== YES/NO AVAILABILITY QUERIES ==========
    if ("available" in query_lower or "stock" in query_lower or "in stock" in query_lower) and is_yes_no_question:
        if "smartwatch" in query_lower:
            return "Yes. SmartWatch Pro X is in stock."
        elif "earbuds" in query_lower:
            return "Yes. Wireless Earbuds Elite is in stock."
        elif "power bank" in query_lower:
            return "Yes. Power Bank Ultra is in stock."
        else:
            return "Yes. All products are currently in stock."
    
    # ========== YES/NO SHIPPING QUERIES ==========
    if ("shipping" in query_lower or "free" in query_lower) and is_yes_no_question:
        if "free" in query_lower:
            return "Yes. Free shipping on orders above ₹5,000."
        return "Yes. Shipping is available. Free on orders above ₹5,000."
    
    # ========== PRICE QUERIES ==========
    if "price" in query_lower or "cost" in query_lower or "how much" in query_lower:
        if "smartwatch" in query_lower or "smartwatch pro x" in query_lower:
            return "₹15,999"
        elif "earbuds" in query_lower or "earbud" in query_lower or "wireless earbuds" in query_lower:
            return "₹7,999"
        elif "power bank" in query_lower or "powerbank" in query_lower:
            return "₹3,499"
    
    # ========== WARRANTY QUERIES ==========
    if "warranty" in query_lower:
        if "extended" in query_lower or "2 year" in query_lower or "two year" in query_lower:
            return "Extended warranty (2 years) costs ₹1,999"
        return "1 year standard warranty. Extended warranty (2 years): ₹1,999"
    
    # ========== BATTERY LIFE QUERIES ==========
    if "battery" in query_lower or "battery life" in query_lower:
        if "smartwatch" in query_lower:
            return "7 days"
        elif "earbuds" in query_lower or "earbud" in query_lower:
            return "20 hours"
        elif "power bank" in query_lower or "powerbank" in query_lower:
            return "30,000mAh capacity"
    
    # ========== FEATURE QUERIES ==========
    if "feature" in query_lower or "features" in query_lower or "what does" in query_lower or "what can" in query_lower:
        if "smartwatch" in query_lower:
            if "heart rate" in query_lower or "heart" in query_lower:
                return "Heart rate monitoring"
            elif "gps" in query_lower:
                return "GPS tracking"
            elif "water" in query_lower:
                return "Water resistant up to 50m"
            return "Heart rate monitoring, GPS tracking, 7-day battery, water resistant (50m)"
        
        elif "earbuds" in query_lower or "earbud" in query_lower:
            if "noise" in query_lower:
                return "Active noise cancellation"
            elif "battery" in query_lower:
                return "20-hour battery life"
            return "Active noise cancellation, premium sound, 20-hour battery, water resistant"
        
        elif "power bank" in query_lower or "powerbank" in query_lower:
            if "capacity" in query_lower:
                return "30,000mAh"
            elif "port" in query_lower or "charging" in query_lower:
                return "Dual USB ports with fast charging support"
            return "30,000mAh capacity, dual USB ports, fast charging, compact design"
    
    # ========== CONTACT/SUPPORT QUERIES ==========
    if any(word in query_lower for word in ["support", "contact", "email", "phone", "reach"]):
        if "hours" in query_lower or "available" in query_lower or "open" in query_lower:
            return "Mon-Sat, 9AM-6PM IST"
        if "email" in query_lower:
            return "support@techgear.com"
        return "Email: support@techgear.com | Hours: Mon-Sat, 9AM-6PM IST"
    
    # ========== RETURN/REFUND QUERIES ==========
    if "return" in query_lower or "refund" in query_lower or "exchange" in query_lower:
        if "window" in query_lower or "days" in query_lower:
            return "7-day return window"
        elif "refund" in query_lower and "days" in query_lower:
            return "5-7 business days"
        elif "shipping" in query_lower:
            return "Free return shipping available"
        return "7-day return window, free shipping, refund in 5-7 business days"
    
    # ========== DEFAULT ==========
    return "Information not available. Please contact support@techgear.com"


# ============================================================================
# NODE 3: ESCALATION
# ============================================================================

def escalation_node(state: SupportState) -> SupportState:
    """
    Escalate query to human support for unknown queries
    """
    
    print("\n" + "=" * 70)
    print("NODE: ESCALATION")
    print("=" * 70)
    print(f"Query: {state['user_query']}")
    print(f"Category: {state['category']} (requires escalation)")
    
    escalation_message = """Your query requires human support. Please contact our support team:

📧 Email: support@techgear.com
🕐 Hours: Mon-Sat, 9AM-6PM IST

We'll get back to you as soon as possible!"""
    
    print(f"Response: Escalation triggered")
    
    return {
        "user_query": state["user_query"],
        "category": state["category"],
        "response": escalation_message
    }


# ============================================================================
# CONDITIONAL ROUTING
# ============================================================================

def route_query(state: SupportState) -> Literal["rag_responder", "escalation"]:
    """
    Route query based on classification:
    - products, returns, general → RAG responder
    - unknown → Escalation
    """
    
    category = state["category"]
    
    print(f"\n[ROUTING] Category: {category}")
    
    if category in ["products", "returns", "general"]:
        print(f"[ROUTING] → RAG Responder")
        return "rag_responder"
    else:
        print(f"[ROUTING] → Escalation")
        return "escalation"


# ============================================================================
# BUILD WORKFLOW
# ============================================================================

def build_support_workflow():
    """
    Build the complete LangGraph workflow for customer support
    
    Workflow Structure:
    
    Entry (Classifier)
         ↓
    Conditional Router
         ├→ [products|returns|general] → RAG Responder → END
         └→ [unknown] → Escalation → END
    """
    
    print("=" * 70)
    print("Building Support Workflow")
    print("=" * 70)
    
    # Create state graph
    workflow = StateGraph(SupportState)
    
    # Add nodes
    print("\n[Building] Adding nodes...")
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("rag_responder", rag_responder_node)
    workflow.add_node("escalation", escalation_node)
    
    print("  ✓ classifier")
    print("  ✓ rag_responder")
    print("  ✓ escalation")
    
    # Set entry point
    print("\n[Building] Setting entry point...")
    workflow.set_entry_point("classifier")
    print("  ✓ Entry: classifier")
    
    # Add conditional routing after classifier
    print("\n[Building] Adding conditional routing...")
    workflow.add_conditional_edges(
        "classifier",
        route_query,
        {
            "rag_responder": "rag_responder",
            "escalation": "escalation"
        }
    )
    print("  ✓ Route: classifier → [rag_responder | escalation]")
    
    # Add edges to END node
    print("\n[Building] Adding terminal edges...")
    workflow.add_edge("rag_responder", END)
    workflow.add_edge("escalation", END)
    
    print("  ✓ rag_responder → END")
    print("  ✓ escalation → END")
    
    # Compile workflow
    print("\n[Building] Compiling workflow...")
    app = workflow.compile()
    
    print("  ✓ Workflow compiled successfully")
    
    print("\n" + "=" * 70)
    print("Workflow Ready!")
    print("=" * 70)
    
    return app


# ============================================================================
# MAIN (for testing)
# ============================================================================

def run_workflow(app, user_query):
    """Run the workflow with a user query"""
    
    print(f"User Query: {user_query}\n")
    
    # Initialize state
    initial_state = {
        "user_query": user_query,
        "category": "",
        "response": ""
    }
    
    # Run workflow
    result = app.invoke(initial_state)
    
    # Display final result
    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)
    print(f"\nFinal Response:\n{result['response']}")
    print(f"\nQuery Category: {result['category']}")
    
    return result


def main():
    """Main function demonstrating the workflow"""
    
    try:
        # Build the workflow
        app = build_support_workflow()
        
        # Test queries
        test_queries = [
            "What products do you sell?",
            "What is the price of SmartWatch Pro X?",
            "Can I return my product within 30 days?",
            "What are your support hours?",
            "Tell me about your company's AI capabilities"
        ]
        
        # Run workflow for each query
        for i, query in enumerate(test_queries, 1):
            print(f"\n\n{'█' * 70}")
            print(f"TEST QUERY {i}/{len(test_queries)}")
            print(f"{'█' * 70}")
            
            result = run_workflow(app, query)
            
            if i < len(test_queries):
                print("\n" + "─" * 70)
    
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
