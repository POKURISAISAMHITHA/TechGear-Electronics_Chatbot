"""
LangGraph Workflow Demo: Shows workflow structure and routing without API dependency
Demonstrates the complete flow: Classifier → Routing → RAG/Escalation → END
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Import the actual RAG chain
try:
    from rag_chain import create_rag_chain
    RAG_CHAIN_AVAILABLE = True
except Exception as e:
    print(f"Warning: RAG chain not available: {e}")
    RAG_CHAIN_AVAILABLE = False


# ============================================================================
# STATE DEFINITION
# ============================================================================

class SupportState(TypedDict):
    """State for the customer support workflow"""
    user_query: str
    category: str  # products, returns, general, unknown
    response: str


# ============================================================================
# NODE 1: CLASSIFIER (Mock - No API calls)
# ============================================================================

def classifier_node(state: SupportState) -> SupportState:
    """
    Classify user query into categories
    Mock implementation for demonstration (no Gemini API calls)
    """
    
    print("\n" + "=" * 70)
    print("NODE: CLASSIFIER")
    print("=" * 70)
    print(f"Query: {state['user_query']}")
    
    # Simple keyword-based classification (no API calls)
    query_lower = state["user_query"].lower()
    
    if any(word in query_lower for word in ["price", "cost", "feature", "product", "smartwatch", "earbuds", "power bank"]):
        category = "products"
    elif any(word in query_lower for word in ["return", "refund", "exchange", "policy"]):
        category = "returns"
    elif any(word in query_lower for word in ["support", "hours", "contact", "help", "email"]):
        category = "general"
    else:
        category = "unknown"
    
    print(f"Classified as: {category}")
    
    return {
        "user_query": state["user_query"],
        "category": category,
        "response": state.get("response", "")
    }


# ============================================================================
# NODE 2: RAG RESPONDER
# ============================================================================

# Initialize RAG chain once (global state)
_rag_chain = None

def get_rag_chain():
    """Get or create RAG chain (singleton pattern)"""
    global _rag_chain
    if _rag_chain is None and RAG_CHAIN_AVAILABLE:
        try:
            _rag_chain = create_rag_chain()
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
    return _rag_chain

def rag_responder_node(state: SupportState) -> SupportState:
    """
    Use RAG chain to generate response for known query categories
    Uses actual RAG chain if available, otherwise uses concise mock responses
    """
    
    print("\n" + "=" * 70)
    print("NODE: RAG RESPONDER")
    print("=" * 70)
    print(f"Query: {state['user_query']}")
    print(f"Category: {state['category']}")
    
    # Try to use actual RAG chain
    rag_chain = get_rag_chain()
    
    if rag_chain:
        try:
            # Use the RAG chain with the improved prompt for concise answers
            response = rag_chain.invoke(state['user_query'])
            print(f"Response generated: {response[:80]}...")
        except Exception as e:
            print(f"Error using RAG chain: {e}")
            print(f"Falling back to concise mock responses...")
            response = _get_concise_response(state['user_query'])
    else:
        # Use concise mock responses if RAG chain unavailable
        print(f"RAG chain unavailable, using concise mock responses...")
        response = _get_concise_response(state['user_query'])
    
    return {
        "user_query": state["user_query"],
        "category": state["category"],
        "response": response
    }


def _get_concise_response(query: str) -> str:
    """
    Generate CONCISE, SPECIFIC responses - answer ONLY what was asked
    NO full descriptions unless explicitly asked
    """
    query_lower = query.lower()
    
    # ========== PRODUCT LISTING QUERIES ==========
    if any(word in query_lower for word in ["sell", "product", "products", "catalogue", "catalog", "available", "offer", "have"]):
        if "list" in query_lower or "what" in query_lower or "which" in query_lower or "do you" in query_lower or "sell" in query_lower:
            return """We sell the following products:

1. **SmartWatch Pro X** - ₹15,999
   Heart rate monitoring, GPS tracking, 7-day battery, water resistant (50m)

2. **Wireless Earbuds Elite** - ₹7,999
   Active noise cancellation, 20-hour battery, premium sound, water resistant

3. **Power Bank Ultra** - ₹3,499
   30,000mAh capacity, dual USB ports, fast charging, compact design"""
    
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
    
    # ========== FEATURE QUERIES - SPECIFIC FEATURES ==========
    if "feature" in query_lower or "features" in query_lower or "what does" in query_lower or "what can" in query_lower:
        if "smartwatch" in query_lower:
            if "heart rate" in query_lower or "heart" in query_lower:
                return "Yes, heart rate monitoring available"
            elif "gps" in query_lower:
                return "Yes, GPS tracking included"
            elif "water" in query_lower:
                return "Water resistant up to 50m"
            return "Heart rate monitoring, GPS tracking, 7-day battery, water resistant (50m)"
        
        elif "earbuds" in query_lower or "earbud" in query_lower:
            if "noise" in query_lower:
                return "Yes, active noise cancellation included"
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
    
    # ========== LOCATION QUERIES ==========
    if "location" in query_lower or "address" in query_lower or "where are you" in query_lower:
        return "TechGear Headquarters, India"
    
    # ========== AVAILABILITY QUERIES ==========
    if "available" in query_lower or "in stock" in query_lower:
        return "All products currently in stock"
    
    # ========== PAYMENT QUERIES ==========
    if "payment" in query_lower or "pay" in query_lower or "accept" in query_lower:
        return "We accept all major credit cards, debit cards, and digital wallets"
    
    # ========== SHIPPING QUERIES ==========
    if "shipping" in query_lower or "delivery" in query_lower or "ship" in query_lower:
        if "free" in query_lower:
            return "Free shipping on orders above ₹5,000"
        elif "time" in query_lower or "how long" in query_lower or "days" in query_lower:
            return "3-5 business days"
        return "3-5 business days delivery, free shipping on orders above ₹5,000"
    
    # ========== WARRANTY CLAIM QUERIES ==========
    if "claim" in query_lower or "repair" in query_lower or "defect" in query_lower or "broken" in query_lower:
        return "Contact support@techgear.com with product serial number for warranty claim"
    
    # ========== COMPARISON QUERIES ==========
    if "smartwatch" in query_lower and "earbuds" in query_lower:
        return "SmartWatch Pro X (₹15,999) vs Wireless Earbuds Elite (₹7,999) - choose based on your needs"
    
    # ========== DISCOUNT/OFFER QUERIES ==========
    if "discount" in query_lower or "offer" in query_lower or "deal" in query_lower or "sale" in query_lower:
        return "Check our website for current promotions and seasonal offers"
    
    # ========== DEFAULT ==========
    return "Information not available. Please contact support@techgear.com or call our support team Mon-Sat, 9AM-6PM IST"


# ============================================================================
# NODE 3: ESCALATION
# ============================================================================

def escalation_node(state: SupportState) -> SupportState:
    """
    Escalate query to human support for unknown or complex queries
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
# EXECUTION
# ============================================================================

def run_workflow(app, user_query: str):
    """
    Run the workflow with a user query
    """
    
    print("\n" + "=" * 70)
    print("EXECUTING WORKFLOW")
    print("=" * 70)
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


# ============================================================================
# WORKFLOW VISUALIZATION
# ============================================================================

def print_workflow_structure():
    """Print the workflow structure"""
    
    print("\n" + "=" * 70)
    print("WORKFLOW STRUCTURE")
    print("=" * 70)
    
    workflow_diagram = """
    
    ┌─────────────────────────────────────────────────────────────┐
    │                     ENTRY POINT                              │
    │                    (User Query)                              │
    └────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
    ┌─────────────────────────────────────────────────────────────┐
    │                    NODE 1: CLASSIFIER                        │
    │  ✓ Input: user_query                                         │
    │  ✓ Logic: Keyword-based classification                      │
    │  ✓ Output: category (products|returns|general|unknown)      │
    └────────────────────────┬────────────────────────────────────┘
                             │
        ╔════════════════════╩════════════════════╗
        │     CONDITIONAL ROUTING               │
        ╚════════════════════╦════════════════════╝
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    products/returns/      general          unknown
    general → ?                                 │
          │                  │                 ↓
          │                  └──→┌──────────────────────────┐
          │                      │  NODE 3: ESCALATION      │
          │                      │  ✓ Returns escalation    │
          │                      │    message to support    │
          │                      │  ✓ Output: response      │
          │                      └──────────┬───────────────┘
          │                                 │
          ↓                                 │
    ┌─────────────────────────┐             │
    │ NODE 2: RAG RESPONDER   │             │
    │ ✓ Uses RAG chain        │             │
    │ ✓ Retrieves docs        │             │
    │ ✓ Generates answer      │             │
    │ ✓ Output: response      │             │
    └──────────┬──────────────┘             │
               │                             │
               └──────────────┬──────────────┘
                              │
                              ↓
              ┌───────────────────────────────┐
              │       EXIT POINT (END)         │
              │    Return Final Response       │
              └───────────────────────────────┘
    """
    
    print(workflow_diagram)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function demonstrating the workflow"""
    
    try:
        # Print workflow structure
        print_workflow_structure()
        
        # Build the workflow
        print("\n\n")
        app = build_support_workflow()
        
        # Test queries
        test_queries = [
            ("What is the price of SmartWatch Pro X?", "products"),
            ("Can I return my product within 30 days?", "returns"),
            ("What are your support hours?", "general"),
            ("Tell me about your company's AI capabilities", "unknown")
        ]
        
        # Run workflow for each query
        for i, (query, expected_category) in enumerate(test_queries, 1):
            print(f"\n\n{'█' * 70}")
            print(f"TEST QUERY {i}/{len(test_queries)}")
            print(f"Expected Category: {expected_category}")
            print(f"{'█' * 70}")
            
            result = run_workflow(app, query)
            
            # Verify routing
            if result["category"] == expected_category:
                print(f"\n✅ Routing Correct: {result['category']} → ", end="")
                if result["category"] == "unknown":
                    print("ESCALATION")
                else:
                    print("RAG RESPONDER")
            else:
                print(f"\n⚠️  Routing Note: Expected {expected_category}, got {result['category']}")
        
        print(f"\n\n{'=' * 70}")
        print("All Tests Complete!")
        print(f"{'=' * 70}\n")
        
        return app
    
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    app = main()
