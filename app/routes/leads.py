"""
Lead management routes
"""

from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.core.client import c2s_client
from app.models.schemas import (
    ActivityCreate,
    DoneDeal,
    LeadCreate,
    LeadForward,
    LeadTagCreate,
    LeadUpdate,
    MessageCreate,
    VisitCreate,
)

router = APIRouter(prefix="/leads", tags=["Leads"])

# =============================================================================
# RESOLVE SOURCE - Must be before /{lead_id} route to avoid conflicts
# =============================================================================

IBVI_ADS_GATEWAY_URL = "https://ibvi-ads-gateway.fly.dev"


@router.get("/resolve-source")
async def resolve_lead_source(
    form_id: Optional[str] = Query(None, description="Google Ads Lead Form ID"),
    ad_group_id: Optional[str] = Query(None, description="Google Ads Ad Group ID"),
    campaign_id: Optional[str] = Query(None, description="Google Ads Campaign ID"),
    google_lead_id: Optional[str] = Query(None, description="Google Ads Lead ID (hash)"),
):
    """
    Resolve form_id/ad_group_id to human-readable names.

    Proxies to ibvi-ads-gateway which has Google Ads API access.

    Used by mbras-c2s to get proper product.description for leads.

    Returns:
    {
        "ad_group_id": "187145758017",
        "ad_group_name": "Casa Jardim Europa - Condominio",
        "campaign_name": "Campanha Stoc MBRAS 2025",
        "form_headline": "Casas em Condominio SP",
        "product_description": "Casa Jardim Europa - Condominio"
    }
    """
    try:
        params = {}
        if form_id:
            params["form_id"] = form_id
        if ad_group_id:
            params["ad_group_id"] = ad_group_id
        if campaign_id:
            params["campaign_id"] = campaign_id
        if google_lead_id:
            params["google_lead_id"] = google_lead_id

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{IBVI_ADS_GATEWAY_URL}/v1/leads/resolve-source",
                params=params,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error calling ibvi-ads-gateway: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# STANDARD LEAD ROUTES
# =============================================================================


@router.get("")
async def list_leads(
    page: int = Query(default=1, ge=1),
    perpage: int = Query(default=50, ge=1, le=50),
    sort: Optional[str] = Query(
        None, description="Sort: -created_at, created_at, -updated_at, updated_at"
    ),
    created_gte: Optional[str] = Query(None, description="Created >= (ISO 8601)"),
    created_lt: Optional[str] = Query(None, description="Created < (ISO 8601)"),
    updated_gte: Optional[str] = Query(None, description="Updated >= (ISO 8601)"),
    updated_lt: Optional[str] = Query(None, description="Updated < (ISO 8601)"),
    status: Optional[str] = Query(None, description="Status filter"),
    phone: Optional[str] = None,
    email: Optional[str] = None,
    tags: Optional[str] = None,
):
    """
    List leads with filtering and pagination

    Status options: novo, em_negociacao, convertido, negocio_fechado,
                   arquivado, resgatado, pendente, recusado, finalizado
    """
    try:
        return await c2s_client.get_leads(
            page=page,
            perpage=perpage,
            sort=sort,
            created_gte=created_gte,
            created_lt=created_lt,
            updated_gte=updated_gte,
            updated_lt=updated_lt,
            status=status,
            phone=phone,
            email=email,
            tags=tags,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}")
async def get_lead(lead_id: str):
    """Get specific lead details"""
    try:
        return await c2s_client.get_lead(lead_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_lead(lead: LeadCreate):
    """Create new lead"""
    try:
        return await c2s_client.create_lead(lead.model_dump(exclude_none=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{lead_id}")
async def update_lead(lead_id: str, lead: LeadUpdate):
    """Update lead information"""
    try:
        return await c2s_client.update_lead(lead_id, lead.model_dump(exclude_none=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{lead_id}/forward")
async def forward_lead(lead_id: str, data: LeadForward):
    """Transfer lead to another seller"""
    try:
        return await c2s_client.forward_lead(lead_id, data.seller_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}/tags")
async def get_lead_tags(lead_id: str):
    """Get tags associated with lead"""
    try:
        return await c2s_client.get_lead_tags(lead_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/tags")
async def create_lead_tag(lead_id: str, data: LeadTagCreate):
    """Associate tag with lead"""
    try:
        return await c2s_client.create_lead_tag(lead_id, data.tag_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/mark-interacted")
async def mark_as_interacted(lead_id: str):
    """Mark lead as interacted"""
    try:
        return await c2s_client.mark_lead_as_interacted(lead_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/messages")
async def create_message(lead_id: str, message: MessageCreate):
    """Add message to lead"""
    try:
        return await c2s_client.create_message(lead_id, message.message, message.type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/visits")
async def create_visit(lead_id: str, visit: VisitCreate):
    """Schedule visit for lead"""
    try:
        return await c2s_client.create_visit(
            lead_id, visit.visit_date, visit.description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/activities")
async def create_activity(lead_id: str, activity: ActivityCreate):
    """Log activity for lead"""
    try:
        return await c2s_client.create_activity(
            lead_id, activity.type, activity.description, activity.date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/done-deal")
async def mark_done_deal(lead_id: str, deal: DoneDeal):
    """Mark lead as closed deal"""
    try:
        return await c2s_client.mark_done_deal(lead_id, deal.value, deal.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
