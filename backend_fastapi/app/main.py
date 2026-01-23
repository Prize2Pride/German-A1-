"""
Prize2Pride German A1-A2 Platform - FastAPI Backend
Protocol: OMEGA 777
Author: Manus AI
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from app.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Prize2Pride German Platform API",
    description="High-performance e-learning platform for German A1-A2 learners",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "Prize2Pride German Platform API",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/status")
async def status():
    """
    Detailed status endpoint
    """
    return {
        "status": "operational",
        "database": "connected",
        "cache": "operational",
        "api_version": "1.0.0",
        "protocol": "OMEGA 777",
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Lerne Deutsch, bevor das Bier warm wird!",
        "platform": "Prize2Pride German A1-A2",
        "professor": "Professor Roued",
        "api_version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }

# ============================================================================
# INCLUDE ROUTES
# ============================================================================

from app.routes import include_routes
include_routes(app)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup
    """
    logger.info("🚀 Prize2Pride German Platform API starting...")
    logger.info("Protocol: OMEGA 777")
    logger.info("Professor Roued: Ready to teach!")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on shutdown
    """
    logger.info("🛑 Prize2Pride German Platform API shutting down...")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
