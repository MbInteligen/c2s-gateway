"""
C2S Gateway - Entry Point
Run this file to start the gateway server
"""

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.c2s_gateway_port,
        reload=True,
        log_level="info",
    )
