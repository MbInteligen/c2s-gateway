"""
Webhook management routes
"""

from fastapi import APIRouter, HTTPException

from app.core.client import c2s_client
from app.models.schemas import WebhookSubscribe, WebhookUnsubscribe

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/subscribe")
async def subscribe_webhook(data: WebhookSubscribe):
    """
    Subscribe to lead events via webhook

    Available events:
    - lead.created
    - lead.updated
    - lead.status_changed
    - lead.assigned
    - lead.message_created
    - lead.activity_created
    """
    try:
        return await c2s_client.subscribe_webhook(data.url, data.events)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unsubscribe")
async def unsubscribe_webhook(data: WebhookUnsubscribe):
    """Unsubscribe from lead events"""
    try:
        return await c2s_client.unsubscribe_webhook(data.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
