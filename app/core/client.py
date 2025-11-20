"""
Contact2Sale API Client
"""

import logging
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class C2SClient:
    """Contact2Sale API client for all API operations"""

    def __init__(self):
        self.base_url = settings.c2s_base_url
        self.token = settings.c2s_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        logger.info(f"C2S Client initialized with base URL: {self.base_url}")

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to C2S API"""
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            logger.debug(f"{method} {url} - Params: {params} - Data: {json_data}")

            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30.0,
            )

            response.raise_for_status()
            return response.json()

    # ========== LEADS MANAGEMENT ==========

    async def get_leads(
        self,
        page: int = 1,
        perpage: int = 50,
        sort: Optional[str] = None,
        created_gte: Optional[str] = None,
        created_lt: Optional[str] = None,
        updated_gte: Optional[str] = None,
        updated_lt: Optional[str] = None,
        status: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve leads with filtering and pagination"""
        params = {
            "page": page,
            "perpage": min(perpage, 50),  # Max 50 per page
        }

        if sort:
            params["sort"] = sort
        if created_gte:
            params["created_gte"] = created_gte
        if created_lt:
            params["created_lt"] = created_lt
        if updated_gte:
            params["updated_gte"] = updated_gte
        if updated_lt:
            params["updated_lt"] = updated_lt
        if status:
            params["status"] = status
        if phone:
            params["phone"] = phone
        if email:
            params["email"] = email
        if tags:
            params["tags"] = tags

        return await self._request("GET", "/integration/leads", params=params)

    async def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """Get specific lead details"""
        return await self._request("GET", f"/integration/leads/{lead_id}")

    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new lead"""
        return await self._request("POST", "/integration/leads", json_data=lead_data)

    async def update_lead(
        self, lead_id: str, lead_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update lead information"""
        return await self._request(
            "PATCH", f"/integration/leads/{lead_id}", json_data=lead_data
        )

    async def forward_lead(self, lead_id: str, seller_id: str) -> Dict[str, Any]:
        """Transfer lead to another seller"""
        return await self._request(
            "PATCH",
            f"/integration/leads/{lead_id}/forward",
            json_data={"seller_id": seller_id},
        )

    async def get_lead_tags(self, lead_id: str) -> Dict[str, Any]:
        """Get tags associated with a lead"""
        return await self._request("GET", f"/integration/leads/{lead_id}/tags")

    async def create_lead_tag(self, lead_id: str, tag_id: str) -> Dict[str, Any]:
        """Associate tag with lead"""
        return await self._request(
            "POST",
            f"/integration/leads/{lead_id}/create_tag",
            json_data={"tag_id": tag_id},
        )

    async def mark_lead_as_interacted(self, lead_id: str) -> Dict[str, Any]:
        """Mark lead as interacted"""
        return await self._request(
            "POST", f"/integration/leads/{lead_id}/mark_as_interacted"
        )

    # ========== MESSAGES & ACTIVITIES ==========

    async def create_message(
        self, lead_id: str, message: str, message_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add message to lead"""
        data = {"message": message}
        if message_type:
            data["type"] = message_type
        return await self._request(
            "POST", f"/integration/leads/{lead_id}/create_message", json_data=data
        )

    async def mark_done_deal(
        self, lead_id: str, value: float, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Mark lead as closed deal"""
        data = {"value": value}
        if description:
            data["description"] = description
        return await self._request(
            "POST", f"/integration/leads/{lead_id}/done_deal", json_data=data
        )

    async def create_visit(
        self, lead_id: str, visit_date: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Schedule visit for lead"""
        data = {"visit_date": visit_date}
        if description:
            data["description"] = description
        return await self._request(
            "POST", f"/integration/leads/{lead_id}/create_visit", json_data=data
        )

    async def create_activity(
        self,
        lead_id: str,
        activity_type: str,
        description: str,
        date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Log activity for lead"""
        data = {
            "type": activity_type,
            "description": description,
        }
        if date:
            data["date"] = date
        return await self._request(
            "POST", f"/integration/leads/{lead_id}/create_activity", json_data=data
        )

    # ========== TAGS MANAGEMENT ==========

    async def create_tag(self, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create company tag"""
        return await self._request("POST", "/integration/tags", json_data=tag_data)

    async def get_tags(
        self, name: Optional[str] = None, autofill: Optional[bool] = None
    ) -> Dict[str, Any]:
        """List tags with optional filters"""
        params = {}
        if name:
            params["name"] = name
        if autofill is not None:
            params["autofill"] = autofill
        return await self._request("GET", "/integration/tags", params=params)

    # ========== SELLERS MANAGEMENT ==========

    async def get_sellers(self) -> Dict[str, Any]:
        """List all sellers"""
        return await self._request("GET", "/integration/sellers")

    async def create_seller(self, seller_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new seller"""
        return await self._request(
            "POST", "/integration/sellers", json_data=seller_data
        )

    async def update_seller(
        self, seller_id: str, seller_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update seller configuration"""
        return await self._request(
            "PUT", f"/integration/sellers/{seller_id}", json_data=seller_data
        )

    # ========== DISTRIBUTION QUEUES ==========

    async def get_distribution_queues(self) -> Dict[str, Any]:
        """List all distribution queues"""
        return await self._request("GET", "/integration/distribution_queues")

    async def redistribute_lead(
        self, queue_id: str, lead_id: str, seller_id: str
    ) -> Dict[str, Any]:
        """Reassign lead in distribution queue"""
        return await self._request(
            "POST",
            f"/integration/distribution_queues/{queue_id}/redistribute",
            json_data={"lead_id": lead_id, "seller_id": seller_id},
        )

    async def get_queue_sellers(self, queue_id: str) -> Dict[str, Any]:
        """Get sellers in distribution queue"""
        return await self._request(
            "GET", f"/integration/distribution_queues/{queue_id}/sellers"
        )

    async def update_seller_priority(
        self, queue_id: str, seller_id: str, priority: int
    ) -> Dict[str, Any]:
        """Update seller priority in queue"""
        return await self._request(
            "POST",
            f"/integration/distribution_queues/{queue_id}/priority",
            json_data={"seller_id": seller_id, "priority": priority},
        )

    async def set_next_seller(self, queue_id: str, seller_id: str) -> Dict[str, Any]:
        """Define next seller in queue"""
        return await self._request(
            "POST",
            f"/integration/distribution_queues/{queue_id}/next_seller",
            json_data={"seller_id": seller_id},
        )

    # ========== DISTRIBUTION RULES ==========

    async def create_distribution_rule(
        self, rule_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create distribution rule"""
        return await self._request(
            "POST", "/integration/distribution_rules", json_data=rule_data
        )

    # ========== COMPANY & USER INFO ==========

    async def get_me(self) -> Dict[str, Any]:
        """Get user's company details and sub-companies"""
        return await self._request("GET", "/integration/me")

    # ========== WEBHOOKS ==========

    async def subscribe_webhook(
        self, webhook_url: str, events: List[str]
    ) -> Dict[str, Any]:
        """Subscribe to lead events via webhook"""
        return await self._request(
            "POST",
            "/integration/webhook/leads/subscribe",
            json_data={"url": webhook_url, "events": events},
        )

    async def unsubscribe_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Unsubscribe from lead events"""
        return await self._request(
            "POST",
            "/integration/webhook/leads/unsubscribe",
            json_data={"url": webhook_url},
        )


# Global client instance
c2s_client = C2SClient()
