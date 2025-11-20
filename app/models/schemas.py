"""
Pydantic models for C2S Gateway
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

# ========== LEAD MODELS ==========


class LeadCreate(BaseModel):
    """Schema for creating a new lead"""

    customer: str = Field(..., description="Customer name")
    phone: Optional[str] = Field(None, description="Customer phone")
    email: Optional[str] = Field(None, description="Customer email")
    product: Optional[str] = Field(None, description="Product of interest")
    description: Optional[str] = Field(None, description="Lead description")
    source: Optional[str] = Field(None, description="Lead source")
    seller_id: Optional[str] = Field(None, description="Assigned seller ID")


class LeadUpdate(BaseModel):
    """Schema for updating lead information"""

    customer: Optional[str] = None
    product: Optional[str] = None
    description: Optional[str] = None


class LeadForward(BaseModel):
    """Schema for forwarding lead to another seller"""

    seller_id: str = Field(..., description="Target seller ID")


class LeadQuery(BaseModel):
    """Query parameters for listing leads"""

    page: int = Field(default=1, ge=1)
    perpage: int = Field(default=50, ge=1, le=50)
    sort: Optional[str] = Field(
        None, description="Sort field: -created_at, created_at, -updated_at, updated_at"
    )
    created_gte: Optional[str] = Field(None, description="Created date >= (ISO 8601)")
    created_lt: Optional[str] = Field(None, description="Created date < (ISO 8601)")
    updated_gte: Optional[str] = Field(None, description="Updated date >= (ISO 8601)")
    updated_lt: Optional[str] = Field(None, description="Updated date < (ISO 8601)")
    status: Optional[str] = Field(None, description="Lead status filter")
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[str] = None


# ========== MESSAGE MODELS ==========


class MessageCreate(BaseModel):
    """Schema for creating a message"""

    message: str = Field(..., description="Message content")
    type: Optional[str] = Field(None, description="Message type")


# ========== ACTIVITY MODELS ==========


class VisitCreate(BaseModel):
    """Schema for creating a visit"""

    visit_date: str = Field(..., description="Visit date (ISO 8601)")
    description: Optional[str] = None


class ActivityCreate(BaseModel):
    """Schema for creating an activity"""

    type: str = Field(..., description="Activity type")
    description: str = Field(..., description="Activity description")
    date: Optional[str] = Field(None, description="Activity date (ISO 8601)")


class DoneDeal(BaseModel):
    """Schema for marking deal as done"""

    value: float = Field(..., description="Deal value", gt=0)
    description: Optional[str] = None


# ========== TAG MODELS ==========


class TagCreate(BaseModel):
    """Schema for creating a tag"""

    name: str = Field(..., description="Tag name")
    autofill: Optional[bool] = Field(False, description="Auto-fill tag")
    color: Optional[str] = Field(None, description="Tag color (hex)")


class LeadTagCreate(BaseModel):
    """Schema for associating tag with lead"""

    tag_id: str = Field(..., description="Tag ID to associate")


# ========== SELLER MODELS ==========


class SellerCreate(BaseModel):
    """Schema for creating a seller"""

    name: str = Field(..., description="Seller name")
    email: str = Field(..., description="Seller email")
    phone: Optional[str] = None
    active: Optional[bool] = Field(True, description="Seller active status")


class SellerUpdate(BaseModel):
    """Schema for updating seller"""

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    active: Optional[bool] = None


# ========== DISTRIBUTION MODELS ==========


class LeadRedistribute(BaseModel):
    """Schema for redistributing lead"""

    lead_id: str = Field(..., description="Lead ID to redistribute")
    seller_id: str = Field(..., description="Target seller ID")


class SellerPriority(BaseModel):
    """Schema for updating seller priority"""

    seller_id: str = Field(..., description="Seller ID")
    priority: int = Field(..., description="Priority level", ge=0)


class NextSeller(BaseModel):
    """Schema for setting next seller"""

    seller_id: str = Field(..., description="Seller ID")


class DistributionRuleCreate(BaseModel):
    """Schema for creating distribution rule"""

    name: str = Field(..., description="Rule name")
    queue_id: str = Field(..., description="Distribution queue ID")
    conditions: dict = Field(..., description="Rule conditions")
    actions: dict = Field(..., description="Rule actions")


# ========== WEBHOOK MODELS ==========


class WebhookSubscribe(BaseModel):
    """Schema for webhook subscription"""

    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(..., description="Events to subscribe to")


class WebhookUnsubscribe(BaseModel):
    """Schema for webhook unsubscription"""

    url: str = Field(..., description="Webhook URL to unsubscribe")


# ========== TEST MODELS (marked with TEST) ==========


class TestLeadCreate(BaseModel):
    """TEST SCHEMA - Schema for creating test leads"""

    customer: str = Field(default="TEST Customer", description="TEST customer name")
    phone: Optional[str] = Field(default="+55119TEST1234", description="TEST phone")
    email: Optional[str] = Field(default="test@example.com", description="TEST email")
    product: Optional[str] = Field(default="TEST Product", description="TEST product")
    description: Optional[str] = Field(
        default="TEST lead created by C2S Gateway", description="TEST description"
    )
    source: Optional[str] = Field(default="TEST_GATEWAY", description="TEST source")


class TestMessageCreate(BaseModel):
    """TEST SCHEMA - Schema for creating test messages"""

    message: str = Field(
        default="TEST message from C2S Gateway", description="TEST message content"
    )
    type: Optional[str] = Field(default="note", description="TEST message type")
