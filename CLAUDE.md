# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**C2S Gateway** - Contact2Sale CRM API Gateway for MBRAS/IBVI lead management system. This FastAPI service provides a unified interface to the Contact2Sale CRM, handling lead enrichment from Google Ads campaigns and property mapping.

**Key Purpose**: Prevent "Não identificado" leads by enriching Google Ads webhook data with property details before sending to Contact2Sale CRM.

## Architecture

### System Context
```
Google Ads Lead Form
    ↓ webhook
IBVI Platform (webhook handler)
    ↓ enrichment
C2S Gateway (THIS SERVICE)
    ↓ API calls
Contact2Sale CRM
```

### Service Architecture
- **Framework**: FastAPI with async/await patterns
- **HTTP Client**: httpx for async API calls
- **Validation**: Pydantic models for request/response validation
- **Configuration**: Environment-based config with validation
- **Deployment**: Fly.io with GitHub Actions CI/CD

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with C2S credentials

# Run development server with auto-reload
uvicorn app.main:app --reload --port 8000

# Run without reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing & Validation
```bash
# Test campaign enricher
python campaign_enricher.py

# Test specific lead creation scripts
python create_guilherme_lux600.py
python get_30_latest_leads.py

# Check API documentation
# Visit http://localhost:8000/docs (Swagger UI)
# Visit http://localhost:8000/redoc (ReDoc)
```

### Deployment
```bash
# Deploy to Fly.io (auto-triggered on push to main)
fly deploy

# Manual deployment
fly deploy --app mbras-c2s-gateway

# Check deployment status
fly status --app mbras-c2s-gateway
fly logs --app mbras-c2s-gateway

# Update secrets
fly secrets set C2S_TOKEN=<new_token> --app mbras-c2s-gateway
fly secrets set C2S_BASE_URL=https://api.contact2sale.com --app mbras-c2s-gateway
```

## Code Organization

### Core Components

**app/core/**
- `config.py`: Environment validation and settings management. Validates C2S_TOKEN and C2S_BASE_URL.
- `client.py`: HTTP client singleton for C2S API communication. Handles authentication and request formatting.

**app/routes/**
- `leads.py`: Lead CRUD operations (28+ endpoints)
- `tags.py`: Tag management
- `sellers.py`: Seller operations
- `distribution.py`: Lead distribution and queue management
- `webhooks.py`: Webhook subscription management
- `company.py`: Company-level operations
- `test.py`: Test endpoints (should be removed in production)

**app/models/**
- Pydantic models for request/response validation
- Ensures type safety across API boundaries

### Campaign Enrichment System

**campaign_enricher.py**: Core enrichment logic
- Maps Google Ads campaign IDs to property details
- Prevents "Não identificado" property issues
- Formats lead data for Contact2Sale

**campaign_mapping.json**: Configuration file
- Maps campaign ID 22866487607 → LUX 600 property
- Contains property details, pricing, features
- Version-controlled configuration

### Utility Scripts

Located in root directory, these scripts interact with the deployed gateway:
- `create_guilherme_lux600.py`: Example of creating enriched lead
- `get_30_latest_leads.py`, `get_16_more_leads.py`: Lead export utilities
- `update_lux600_leads.py`: Batch update operations

## Key Implementation Details

### Environment Validation
The service enforces strict validation:
- C2S_TOKEN must be non-empty and valid JWT format
- C2S_BASE_URL must start with http:// or https://
- Configuration failures prevent service startup

### Campaign Enrichment Flow
1. Webhook receives Google Ads lead with `campaign_id`
2. CampaignEnricher looks up campaign in mapping
3. If found, enriches with property details (description, price, features)
4. Formats enriched data for C2S API
5. Creates lead with proper attribution (source: "Google Ads")

### API Client Pattern
- Singleton client instance (`c2s_client`)
- Automatic token injection in headers
- Consistent error handling across endpoints
- Async/await for non-blocking operations

### Lead Status Values
```python
STATUS_OPTIONS = [
    "novo", "em_negociacao", "convertido", 
    "negocio_fechado", "arquivado", "resgatado",
    "pendente", "recusado", "finalizado"
]
```

## Current Campaign Mapping

**LUX 600 Campaign** (ID: 22866487607)
- Property: Vila Nova Conceição - Lux 400+m²
- Price Range: R$ 15M - R$ 20M
- Features: Bernardes Arquitetura, Vista Ibirapuera, 397-859m²
- Lead Source ID: 493

## Deployment Details

**Production URL**: https://mbras-c2s-gateway.fly.dev
**Organization**: IBVI (Fly.io)
**Region**: GRU (São Paulo)
**Auto-scaling**: 0-N machines (auto stop/start)
**Health Check**: GET / every 30s

## Common Tasks

### Add New Campaign Mapping
1. Edit `campaign_mapping.json`
2. Add campaign ID with property details
3. Deploy changes (auto via GitHub push to main)

### Debug Failed Leads
1. Check logs: `fly logs --app mbras-c2s-gateway`
2. Verify token is valid: Check C2S_TOKEN secret
3. Test enrichment locally: Run `campaign_enricher.py` with test data

### Update C2S Credentials
```bash
fly secrets set C2S_TOKEN=<new_token> --app mbras-c2s-gateway
# Service will auto-restart with new credentials
```

## Important Notes

- The `/test` router endpoints should be removed before production
- All lead creation should go through enrichment to avoid "Não identificado" properties
- The service maintains no state - all data is passed through to C2S
- Campaign mapping is version-controlled and deployed with the service
- Failed API calls return HTTP 500 with error details for debugging