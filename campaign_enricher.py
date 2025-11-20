#!/usr/bin/env python3
"""
Campaign Enricher for Google Ads Leads
Maps campaign_id to property details for Contact2Sale
"""

import json
from pathlib import Path
from typing import Dict, Optional


class CampaignEnricher:
    """Enrich leads with campaign and property information"""

    def __init__(self, mapping_file: str = "campaign_mapping.json"):
        """Load campaign mapping from JSON file"""
        mapping_path = Path(__file__).parent / mapping_file

        with open(mapping_path, "r", encoding="utf-8") as f:
            self.mapping = json.load(f)

        self.campaigns = self.mapping.get("google_ads_campaigns", {})
        self.default_source = self.mapping.get("default_lead_source", {})

    def enrich_lead(self, webhook_data: Dict) -> Dict:
        """
        Enrich webhook data with campaign and property information

        Args:
            webhook_data: Raw webhook data from Google Ads
            {
                "name": "Customer Name",
                "email": "email@example.com",
                "phone": "+5511999999999",
                "description": "",
                "adgroup_name": "",
                "campaign_id": "22866487607",
                "lead_id": "012de882..."
            }

        Returns:
            Enriched data ready for Contact2Sale API
            {
                "lead": {
                    "customer": {...},
                    "product": {...},
                    "body": "...",
                    "url": "...",
                    ...
                }
            }
        """
        campaign_id = webhook_data.get("campaign_id", "")
        campaign_info = self.campaigns.get(campaign_id, None)

        # Build customer data
        customer_data = {
            "name": webhook_data.get("name", ""),
            "email": webhook_data.get("email", ""),
            "phone": webhook_data.get("phone", ""),
        }

        # Build enriched lead data
        enriched = {"lead": {"customer": customer_data}}

        # If campaign found in mapping, add property details
        if campaign_info:
            property_data = campaign_info.get("property", {})
            product_details = campaign_info.get("product_details", {})

            # Add product information
            enriched["lead"]["product"] = {
                "description": property_data.get("description", ""),
                "prop_ref": property_data.get("prop_ref", ""),
                "price": str(property_data.get("price", "")),
            }

            # Create detailed message
            message_parts = [
                f"📍 Origem: Google Ads Lead Form Extension",
                f"📢 Campanha: {campaign_info.get('campaign_name', '')}",
                f"🔑 Campaign ID: {campaign_id}",
                f"",
                f"🏢 Imóvel: {product_details.get('building_name', '')}",
                f"📌 Localização: {property_data.get('neighbourhood', '')}",
                f"📐 Área: {product_details.get('area', '')}",
                f"🛏️  Quartos: {product_details.get('bedrooms', '')}",
                f"🚗 Garagem: {product_details.get('parking', '')}",
                f"💰 Preço: {property_data.get('price_display', '')}",
            ]

            # Add features if available
            features = product_details.get("features", [])
            if features:
                message_parts.append("")
                message_parts.append("✨ Destaques:")
                for feature in features:
                    message_parts.append(f"  • {feature}")

            enriched["lead"]["body"] = "\n".join(message_parts)

            # Add URL reference
            enriched["lead"]["url"] = (
                f"https://ads.google.com/leads/{webhook_data.get('lead_id', '')}"
            )

        else:
            # Campaign not mapped, use basic info
            enriched["lead"]["body"] = (
                f"Lead Form do Google Ads\n"
                f"Campaign ID: {campaign_id}\n"
                f"Lead ID: {webhook_data.get('lead_id', '')}"
            )

        return enriched

    def get_campaign_info(self, campaign_id: str) -> Optional[Dict]:
        """Get campaign information by ID"""
        return self.campaigns.get(campaign_id, None)

    def add_campaign_mapping(self, campaign_id: str, campaign_data: Dict):
        """Add or update campaign mapping"""
        self.campaigns[campaign_id] = campaign_data
        self.mapping["google_ads_campaigns"] = self.campaigns

        # Save to file
        mapping_path = Path(__file__).parent / "campaign_mapping.json"
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(self.mapping, f, indent=2, ensure_ascii=False)


# Example usage
if __name__ == "__main__":
    enricher = CampaignEnricher()

    # Example webhook data
    webhook_data = {
        "name": "Guilherme Cappi",
        "email": "guilhermegcappi@gmail.com",
        "phone": "+5511932079000",
        "description": "",
        "adgroup_name": "",
        "campaign_id": "22866487607",
        "lead_id": "012de882c979a473ae69a279537c750f",
    }

    # Enrich the lead
    enriched = enricher.enrich_lead(webhook_data)

    print("📧 Original webhook data:")
    print(json.dumps(webhook_data, indent=2))
    print()
    print("✨ Enriched data for C2S:")
    print(json.dumps(enriched, indent=2, ensure_ascii=False))
