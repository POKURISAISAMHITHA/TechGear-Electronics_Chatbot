"""
FastAPI Backend for Customer Support Chatbot
Integrates with LangGraph workflow for intelligent query routing and response generation
"""

import os
import logging
from typing import Optional
from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, ConfigDict, field_validator
from langgraph_workflow import build_support_workflow

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

workflow_app = None

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
                "query": "What is the price of SmartWatch Pro X?"
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "answer": "The SmartWatch Pro X is priced at ₹15,999 with features including heart rate monitoring, GPS tracking, and 7-day battery life.",
                "category": "products",
                "routed_to": "rag_responder"
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
    Chat endpoint for processing user queries
    
    Process:
    1. Receive user query
    2. Pass to LangGraph workflow
    3. Classifier categorizes query
    4. Route to appropriate node (RAG or Escalation)
    5. Return response with metadata
    
    Args:
        request (ChatRequest): Contains user's query
    
    Returns:
        ChatResponse: Contains answer and routing information
    
    Raises:
        HTTPException: If workflow fails or service error occurs
    """
    
    try:
        # Validate workflow is initialized
        if workflow_app is None:
            logger.error("Workflow not initialized")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Workflow service not available"
            )
        
        # Log incoming query
        logger.info(f"Processing query: {request.query[:100]}...")
        
        # Prepare initial state for workflow
        initial_state = {
            "user_query": request.query,
            "category": "",
            "response": ""
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
        
        # Log successful processing
        logger.info(
            f"Query processed - Category: {category}, "
            f"Routed to: {routed_to}"
        )
        
        # Return response
        return ChatResponse(
            answer=answer,
            category=category,
            routed_to=routed_to
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
