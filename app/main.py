"""
C2S Gateway - Contact2Sale API Gateway
FastAPI application for managing Contact2Sale operations
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import company, distribution, leads, sellers, tags, test, webhooks

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="C2S Gateway",
    description="Contact2Sale API Gateway - Unified access to all C2S capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(tags.router)
app.include_router(sellers.router)
app.include_router(distribution.router)
app.include_router(webhooks.router)
app.include_router(company.router)
app.include_router(test.router)  # TEST routes - DELETE after testing


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "C2S Gateway",
        "version": "1.0.0",
        "description": "Contact2Sale API Gateway",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online",
        "c2s_base_url": settings.c2s_base_url,
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "c2s_configured": bool(settings.c2s_token and settings.c2s_base_url),
    }


@app.on_event("startup")
async def startup_event():
    """Startup event - log configuration"""
    logger.info("=" * 60)
    logger.info("C2S Gateway Starting...")
    logger.info(f"C2S Base URL: {settings.c2s_base_url}")
    logger.info(f"C2S Token: {'***' + settings.c2s_token[-10:]}")
    logger.info(f"Gateway Port: {settings.c2s_gateway_port}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("C2S Gateway shutting down...")
