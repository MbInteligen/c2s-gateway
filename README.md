# Contact2Sale API Gateway

FastAPI gateway service for managing Contact2Sale CRM operations including leads, tags, sellers, and distribution queues.

## Features

- **Complete C2S API Coverage**: All 28+ Contact2Sale API endpoints
- **Lead Management**: Create, update, retrieve, and forward leads
- **Campaign Enrichment**: Automatic Google Ads campaign to property mapping
- **Token Validation**: Secure environment variable validation
- **Type Safety**: Full Pydantic models for request/response validation

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and settings management
- **httpx**: Async HTTP client
- **Python 3.11+**

## Environment Variables

Required environment variables:

```env
C2S_TOKEN=your_c2s_jwt_token_here
C2S_BASE_URL=https://api.contact2sale.com
```

**Validation Rules:**
- `C2S_TOKEN`: Cannot be empty, must be valid JWT
- `C2S_BASE_URL`: Must start with `http://` or `https://`

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Health Check
- `GET /` - Service health check

### Leads
- `GET /leads` - List leads with filtering
- `GET /leads/{lead_id}` - Get specific lead
- `POST /leads` - Create new lead
- `PATCH /leads/{lead_id}` - Update lead
- `POST /leads/{lead_id}/forward` - Forward lead to seller
- `POST /leads/{lead_id}/mark_as_interacted` - Mark as interacted

### Messages & Activities
- `POST /leads/{lead_id}/messages` - Add message to lead
- `POST /leads/{lead_id}/done_deal` - Mark as closed deal
- `POST /leads/{lead_id}/visits` - Schedule visit
- `POST /leads/{lead_id}/activities` - Log activity

### Tags
- `GET /tags` - List tags
- `POST /tags` - Create tag
- `GET /leads/{lead_id}/tags` - Get lead tags
- `POST /leads/{lead_id}/tags` - Associate tag with lead

### Sellers
- `GET /sellers` - List sellers
- `POST /sellers` - Create seller
- `PUT /sellers/{seller_id}` - Update seller

### Distribution
- `GET /distribution_queues` - List queues
- `POST /distribution_queues/{queue_id}/redistribute` - Reassign lead
- `GET /distribution_queues/{queue_id}/sellers` - Get queue sellers
- `POST /distribution_queues/{queue_id}/priority` - Update priority
- `POST /distribution_queues/{queue_id}/next_seller` - Set next seller

### Webhooks
- `POST /webhook/subscribe` - Subscribe to events
- `POST /webhook/unsubscribe` - Unsubscribe from events

## Campaign Enrichment

The gateway includes a campaign enrichment system that automatically maps Google Ads campaign IDs to property details:

```python
# campaign_mapping.json
{
  "google_ads_campaigns": {
    "22866487607": {
      "campaign_name": "MBRAS - LUX 600",
      "property": {
        "description": "Vila Nova Conceição - Lux 400+m²",
        "prop_ref": "LUX600",
        "price": "18000000"
      }
    }
  }
}
```

Usage:
```python
from campaign_enricher import CampaignEnricher

enricher = CampaignEnricher()
enriched_data = enricher.enrich_lead(webhook_data)
```

## Deployment

### Fly.io

Deployed automatically via GitHub Actions on push to `main` branch.

```bash
# Manual deployment
fly deploy

# View logs
fly logs

# Check status
fly status
```

### Environment Secrets

Set secrets in Fly.io:
```bash
fly secrets set C2S_TOKEN=your_token_here
fly secrets set C2S_BASE_URL=https://api.contact2sale.com
```

## Project Structure

```
c2s-gateway/
├── app/
│   ├── core/
│   │   ├── config.py          # Environment validation
│   │   └── client.py          # C2S API client
│   ├── models/
│   │   └── lead.py            # Pydantic models
│   ├── routes/
│   │   ├── leads.py           # Lead endpoints
│   │   ├── tags.py            # Tag endpoints
│   │   ├── sellers.py         # Seller endpoints
│   │   └── distribution.py    # Distribution endpoints
│   └── main.py                # FastAPI app
├── campaign_mapping.json      # Campaign to property mapping
├── campaign_enricher.py       # Enrichment logic
├── requirements.txt           # Python dependencies
├── fly.toml                   # Fly.io configuration
└── README.md                  # This file
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contact2Sale API

Official documentation: [Contact2Sale API Docs](https://contact2sale.com/developers)

## License

Proprietary - MbInteligen
