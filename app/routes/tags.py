"""
Tag management routes
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.client import c2s_client
from app.models.schemas import TagCreate

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("")
async def list_tags(
    name: Optional[str] = Query(None, description="Filter by tag name"),
    autofill: Optional[bool] = Query(None, description="Filter by autofill status"),
):
    """List all tags with optional filters"""
    try:
        return await c2s_client.get_tags(name=name, autofill=autofill)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_tag(tag: TagCreate):
    """Create new company tag"""
    try:
        return await c2s_client.create_tag(tag.model_dump(exclude_none=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
