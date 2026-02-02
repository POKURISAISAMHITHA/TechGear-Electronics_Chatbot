"""
FastAPI Backend for Customer Support Chatbot
Integrates with LangGraph workflow for intelligent query routing and response generation
"""

import os
import logging
from typing import Optional, List, Dict
import difflib
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, ConfigDict, field_validator
from langgraph_workflow import build_support_workflow
import uuid

# Load environment variables
load_dotenv()

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# GLOBAL STATE
# ============================================================================

# Global workflow and product list
workflow_app = None

# In-memory product list loaded from product_info.txt for robust extraction
product_names: List[str] = []

# In-memory conversation history storage
# Structure: {session_id: {"history": [{"query": str, "response": str, "timestamp": datetime}], "last_product": str}}
conversation_sessions: Dict[str, Dict] = {}

# Session timeout (30 minutes)
SESSION_TIMEOUT = timedelta(minutes=30)


def clean_expired_sessions():
    """Remove expired conversation sessions"""
    current_time = datetime.now()
    expired_sessions = []
    
    for session_id, session_data in conversation_sessions.items():
        if session_data["history"]:
            last_interaction = session_data["history"][-1]["timestamp"]
            if current_time - last_interaction > SESSION_TIMEOUT:
                expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del conversation_sessions[session_id]
    
    if expired_sessions:
        logger.info(f"Cleaned {len(expired_sessions)} expired sessions")


def load_product_names(filepath: str = "product_info.txt") -> List[str]:
    """Load product names from the product_info.txt file into memory.

    Returns a list of product names found in the file.
    """
    products: List[str] = []
    try:
        repo_root = Path(__file__).parent
        file_path = repo_root / filepath
        if not file_path.exists():
            logger.warning(f"Product info file not found: {file_path}")
            return products

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.lower().startswith("product:"):
                    # Format: Product: Name
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        pname = parts[1].strip()
                        if pname:
                            products.append(pname)
    except Exception as e:
        logger.error(f"Failed to load product names: {e}")
    logger.info(f"Loaded {len(products)} product names from {filepath}")
    return products


def extract_product_name(query: str, answer: str) -> Optional[str]:
    """
    Extract product name from query or answer using simple pattern matching
    
    Args:
        query: User's query (potentially enhanced)
        answer: Bot's response
    
    Returns:
        Product name if detected, None otherwise
    """
    # Common product patterns in queries
    import re
    
    # Patterns to match product names (more comprehensive)
    patterns = [
        # Specific products
        r'Portable\s+Air\s+Compressor',
        r'Smart\s+Luggage\s+Tracker\s+GPS',
        r'Sleep\s+Headphones\s+Bluetooth',
        r'Smartphone\s+Gimbal\s+Stabilizer',
        r'Smart\s+Bike\s+Lock\s+Fingerprint',
        r'Posture\s+Corrector\s+Smart\s+Wearable',
        r'SmartWatch\s+(?:Pro|Classic|Ultra|Fitness)\s+[A-Z\d]+',
        r'TrueSound\s+(?:Pro|Bass|Max)\s*\d*',
        r'UltraBook\s+Pro\s+\d+',
        r'Gaming\s+Laptop\s+[\w\s]+\d+',
        r'Budget\s+Laptop\s+[\w\s]+\d+',
        r'MacBook\s+Style\s+[\w\s]+\d+',
        r'PowerMax\s+\d+',
        r'ActionCam\s+(?:Pro|Ultra)\s*\d*',
        r'DroneX\s+(?:Pro|Mini)\s*[\w\s]*',
        r'Smart\s+[\w\s]+(?:Lock|Speaker|Display|Hub|Camera|Doorbell|Thermostat|Plug|Wearable)',
        r'Portable\s+[\w\s]+(?:Monitor|Compressor|Charger|Speaker)',
        r'Fitness\s+Tracker\s+[\w\s]+',
        r'2-in-1\s+Convertible\s+Laptop',
        r'UltraView\s+\d+K\s+Monitor',
        r'HomeHub\s+Smart\s+Speaker',
        r'Smart\s+Home\s+[\w\s]+Kit',
        r'Wireless\s+Charger\s+[\w\s]+',
        r'Car\s+Mount\s+[\w\s]+',
        r'Phone\s+Stand\s+[\w\s]+',
        r'Laptop\s+Stand\s+[\w\s]+',
        r'USB-C\s+Hub\s+[\w\s]+',
        r'External\s+SSD\s+[\w\s]+\d+\w*',
        r'Mechanical\s+Keyboard\s+[\w\s]+',
        r'Wireless\s+Mouse\s+[\w\s]+',
        r'Gaming\s+Mouse\s+[\w\s]+',
        r'Webcam\s+[\w\s]+\d*[KP]*',
        r'Ring\s+Light\s+[\w\s]+',
        r'Microphone\s+[\w\s]+',
        r'Tablet\s+[\w\s]+\d+',
        r'E-Reader\s+[\w\s]+',
        r'Gimbal\s+Stabilizer\s+[\w\s]*',
        r'Bike\s+Lock\s+[\w\s]*',
        r'Air\s+Compressor[\w\s]*',
        r'Luggage\s+Tracker[\w\s]*',
        r'[\w\s]+Headphones\s+Bluetooth',
        r'Bluetooth\s+Headphones[\w\s]*',
        r'[\w\s]+Corrector\s+[\w\s]+Wearable',
    ]
    
    # First: check against loaded product names (exact/substr match)
    try:
        q_low = query.lower()
        a_low = answer.lower()
        if product_names:
            for prod in product_names:
                plow = prod.lower()
                if plow in q_low or plow in a_low:
                    logger.info(f"Matched product from product list: {prod}")
                    return prod

            # Next: fuzzy match using difflib on combined text
            combined = (query + " " + answer).strip()
            if combined:
                matches = difflib.get_close_matches(combined, product_names, n=1, cutoff=0.6)
                if matches:
                    logger.info(f"Fuzzy matched product: {matches[0]}")
                    return matches[0]
    except Exception:
        pass

    # Regex fallback: check query first (higher priority)
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            product_name = match.group(0).strip()
            logger.info(f"Extracted product from query (regex): {product_name}")
            return product_name

    # If not found in query, check answer
    for pattern in patterns:
        match = re.search(pattern, answer, re.IGNORECASE)
        if match:
            product_name = match.group(0).strip()
            logger.info(f"Extracted product from answer (regex): {product_name}")
            return product_name

    return None

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's question or query"
    )
    session_id: Optional[str] = Field(
        None,
        description="Session ID for maintaining conversation context"
    )

    @field_validator('query')
    @classmethod
    def query_must_not_be_empty(cls, v):
        """Validate that query is not just whitespace"""
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "What is the price of SmartWatch Pro X?",
                "session_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )


class ChatResponse(BaseModel):
    """Response body for chat endpoint"""
    answer: str = Field(
        ...,
        description="Generated response from chatbot"
    )
    category: Optional[str] = Field(
        None,
        description="Query classification (products, returns, general, unknown)"
    )
    routed_to: Optional[str] = Field(
        None,
        description="Node that handled the query (rag_responder, escalation)"
    )
    session_id: str = Field(
        ...,
        description="Session ID for maintaining conversation context"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "answer": "The SmartWatch Pro X is priced at ₹15,999 with features including heart rate monitoring, GPS tracking, and 7-day battery life.",
                "category": "products",
                "routed_to": "rag_responder",
                "session_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )


class HealthResponse(BaseModel):
    """Response body for health check endpoint"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "message": "Chatbot service is running"
            }
        }
    )


# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for FastAPI lifespan events
    Handles startup and shutdown of the workflow
    """
    # STARTUP
    logger.info("Starting chatbot service...")
    try:
        global workflow_app
        workflow_app = build_support_workflow()
        logger.info("✓ LangGraph workflow initialized successfully")
        # Load product names into memory for robust product extraction and follow-up handling
        global product_names
        product_names = load_product_names("product_info.txt")
    except Exception as e:
        logger.error(f"Failed to initialize workflow: {e}")
        raise

    yield

    # SHUTDOWN
    logger.info("Shutting down chatbot service...")
    logger.info("✓ Service shutdown complete")


# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Customer Support Chatbot API",
    description="Intelligent customer support chatbot with LangGraph workflow",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ROUTES
# ============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the chatbot service is running"
)
async def health_check():
    """
    Health check endpoint to verify service status
    
    Returns:
        HealthResponse: Status and message
    """
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        message="Chatbot service is running"
    )


@app.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    tags=["Chat"],
    summary="Send Chat Query",
    description="Send a query to the chatbot and receive a response"
)
async def chat(request: ChatRequest):
    """
    Chat endpoint for processing user queries with conversation memory
    
    Process:
    1. Receive user query and optional session_id
    2. Retrieve conversation history if session exists
    3. Enhance query with context if it's a follow-up question
    4. Pass to LangGraph workflow
    5. Classifier categorizes query
    6. Route to appropriate node (RAG or Escalation)
    7. Store conversation in session
    8. Return response with metadata
    
    Args:
        request (ChatRequest): Contains user's query and optional session_id
    
    Returns:
        ChatResponse: Contains answer, session_id, and routing information
    
    Raises:
        HTTPException: If workflow fails or service error occurs
    """
    
    try:
        # Clean expired sessions periodically
        clean_expired_sessions()
        
        # Validate workflow is initialized
        if workflow_app is None:
            logger.error("Workflow not initialized")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Workflow service not available"
            )
        
        # Get or create session ID
        session_id = request.session_id if request.session_id else str(uuid.uuid4())
        
        # Initialize session if it doesn't exist
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = {
                "history": [],
                "last_product": None
            }
        
        session_data = conversation_sessions[session_id]
        
        # Log incoming query
        logger.info(f"Processing query (session: {session_id[:8]}...): {request.query[:100]}...")
        
        # Check if query is a follow-up question (missing context)
        original_query = request.query
        enhanced_query = request.query
        
        # Keywords and phrases that indicate a follow-up question
        follow_up_indicators = [
            # Pronouns and demonstratives
            "this", "that", "it", "its", "them", "those", "these",
            "that product", "this product", "the product", "same product",
            
            # Question starters without product names
            "what about", "how about", "what", "how", "which", "where",
            
            # Product attributes (when asked alone)
            "colour", "color", "colors", "colours",
            "price", "cost", "pricing",
            "warranty", "guarantee",
            "features", "specs", "specifications",
            "availability", "available", "in stock",
            "size", "weight", "dimensions",
            "battery", "battery life",
            "shipping", "delivery",
            "reviews", "ratings",
            "compatible", "compatibility",
            "return", "refund",
        ]
        
        # If query seems like a follow-up and we have a last product
        query_lower = request.query.lower().strip()
        is_follow_up = False
        
        # Check for follow-up indicators
        for indicator in follow_up_indicators:
            if indicator in query_lower:
                is_follow_up = True
                break
        
        # Additional check: queries that start with question words and are short
        question_starters = ["what", "how", "which", "where", "when", "does", "is", "can", "do", "tell"]
        starts_with_question = any(query_lower.startswith(q) for q in question_starters)
        is_short_query = len(request.query.split()) <= 8
        
        # If it starts with a question word and is short, it's likely a follow-up
        if starts_with_question and is_short_query:
            is_follow_up = True
        
        # IMPORTANT: If we have a last_product and query doesn't mention any product name,
        # it's very likely a follow-up question
        if session_data["last_product"] and not is_follow_up:
            # Check if query contains ANY product name patterns
            has_product_mention = False
            product_keywords = ["smart", "watch", "laptop", "earbuds", "earbud", "power bank", 
                              "camera", "drone", "monitor", "tablet", "speaker", "phone",
                              "keyboard", "mouse", "charger", "gimbal", "stabilizer", "lock",
                              "hub", "display", "tracker", "headphones", "headphone", "bluetooth",
                              "wireless", "gaming", "fitness", "portable", "external", 
                              "compressor", "luggage", "corrector", "wearable"]
            for keyword in product_keywords:
                if keyword in query_lower:
                    has_product_mention = True
                    break
            # Also check against loaded product names
            if not has_product_mention and product_names:
                for pname in product_names:
                    if pname.lower() in query_lower:
                        has_product_mention = True
                        break
            
            # If no product mentioned and we have history, treat as follow-up
            if not has_product_mention and len(session_data["history"]) > 0:
                is_follow_up = True
                logger.info(f"Detected follow-up question (no product name in query, have history)")
        
        if is_follow_up and session_data["last_product"]:
            # Check if product name is NOT already in the query
            last_product_lower = session_data["last_product"].lower()
            if last_product_lower not in query_lower:
                # Enhance query with context
                enhanced_query = f"{request.query} for {session_data['last_product']}"
                logger.info(f"Enhanced query with context: {enhanced_query}")
        
        # Prepare initial state for workflow
        initial_state = {
            "user_query": enhanced_query,
            "category": "",
            "response": "",
            "conversation_history": session_data["history"][-3:] if session_data["history"] else []  # Last 3 exchanges
        }
        
        # Execute workflow
        try:
            result = workflow_app.invoke(initial_state)
        except Exception as e:
            logger.error(f"Workflow execution error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process query"
            )
        
        # Extract results
        answer = result.get("response", "")
        category = result.get("category", "unknown")
        
        # Determine routing node
        routed_to = "escalation" if category == "unknown" else "rag_responder"
        
        # Extract product name from query or answer (simple extraction)
        detected_product = extract_product_name(enhanced_query, answer)
        if detected_product:
            session_data["last_product"] = detected_product
            logger.info(f"Detected product: {detected_product}")
        
        # Store conversation in session
        session_data["history"].append({
            "query": original_query,
            "enhanced_query": enhanced_query if enhanced_query != original_query else None,
            "response": answer,
            "category": category,
            "timestamp": datetime.now()
        })
        
        # Keep only last 10 exchanges to prevent memory bloat
        if len(session_data["history"]) > 10:
            session_data["history"] = session_data["history"][-10:]
        
        # Log successful processing
        logger.info(
            f"Query processed - Category: {category}, "
            f"Routed to: {routed_to}, Session: {session_id[:8]}..."
        )
        
        # Return response
        return ChatResponse(
            answer=answer,
            category=category,
            routed_to=routed_to,
            session_id=session_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@app.get("/", tags=["UI"])
async def root():
    """
    Root endpoint serving the web UI
    
    Returns:
        HTML file with the chatbot interface
    """
    index_path = Path(__file__).parent / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    
    # Fallback API info if UI file not found
    return {
        "service": "Customer Support Chatbot API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health",
        "chat": "/chat",
        "ui": "/index.html"
    }


@app.get("/index.html", tags=["UI"])
async def serve_ui():
    """
    Serve the UI HTML file
    
    Returns:
        HTML file with the chatbot interface
    """
    index_path = Path(__file__).parent / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    
    return {
        "error": "UI file not found",
        "status_code": 404
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions"""
    logger.error(f"Validation error: {exc}")
    return {
        "error": str(exc),
        "status_code": status.HTTP_400_BAD_REQUEST
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }


# ============================================================================
# APPLICATION INFO
# ============================================================================

@app.get("/info", tags=["Info"])
async def app_info():
    """
    Get application information
    
    Returns:
        Dictionary with API endpoints and configuration
    """
    return {
        "name": "Customer Support Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "health": {
                "path": "/health",
                "method": "GET",
                "description": "Health check"
            },
            "chat": {
                "path": "/chat",
                "method": "POST",
                "description": "Send chat query"
            }
        },
        "workflow": {
            "classifier": "Categorizes queries into products|returns|general|unknown",
            "rag_responder": "Generates responses for known query types",
            "escalation": "Routes unknown queries to human support"
        }
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "False").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    # Run server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
