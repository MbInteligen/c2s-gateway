"""
Company and user information routes
"""

from fastapi import APIRouter, HTTPException

from app.core.client import c2s_client

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/me")
async def get_company_info():
    """Get user's company details and sub-companies"""
    try:
        return await c2s_client.get_me()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
