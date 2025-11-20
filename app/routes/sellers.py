"""
Seller management routes
"""

from fastapi import APIRouter, HTTPException

from app.core.client import c2s_client
from app.models.schemas import SellerCreate, SellerUpdate

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.get("")
async def list_sellers():
    """List all sellers"""
    try:
        return await c2s_client.get_sellers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_seller(seller: SellerCreate):
    """Create new seller"""
    try:
        return await c2s_client.create_seller(seller.model_dump(exclude_none=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{seller_id}")
async def update_seller(seller_id: str, seller: SellerUpdate):
    """Update seller configuration"""
    try:
        return await c2s_client.update_seller(
            seller_id, seller.model_dump(exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
