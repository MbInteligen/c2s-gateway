"""
Distribution queue and rules management routes
"""

from fastapi import APIRouter, HTTPException

from app.core.client import c2s_client
from app.models.schemas import (
    DistributionRuleCreate,
    LeadRedistribute,
    NextSeller,
    SellerPriority,
)

router = APIRouter(prefix="/distribution", tags=["Distribution"])


# ========== DISTRIBUTION QUEUES ==========


@router.get("/queues")
async def list_distribution_queues():
    """List all distribution queues"""
    try:
        return await c2s_client.get_distribution_queues()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/queues/{queue_id}/redistribute")
async def redistribute_lead(queue_id: str, data: LeadRedistribute):
    """Reassign lead in distribution queue"""
    try:
        return await c2s_client.redistribute_lead(
            queue_id, data.lead_id, data.seller_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queues/{queue_id}/sellers")
async def get_queue_sellers(queue_id: str):
    """Get sellers in distribution queue"""
    try:
        return await c2s_client.get_queue_sellers(queue_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/queues/{queue_id}/priority")
async def update_seller_priority(queue_id: str, data: SellerPriority):
    """Update seller priority in queue"""
    try:
        return await c2s_client.update_seller_priority(
            queue_id, data.seller_id, data.priority
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/queues/{queue_id}/next-seller")
async def set_next_seller(queue_id: str, data: NextSeller):
    """Define next seller in queue"""
    try:
        return await c2s_client.set_next_seller(queue_id, data.seller_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== DISTRIBUTION RULES ==========


@router.post("/rules")
async def create_distribution_rule(rule: DistributionRuleCreate):
    """Create distribution rule"""
    try:
        return await c2s_client.create_distribution_rule(rule.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
