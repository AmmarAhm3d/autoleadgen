from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings
from ..models import Lead
from ..tools.yelp import search_yelp_businesses


@dataclass
class ScraperAgent:
    settings: Settings

    def discover_leads(self, *, query: str, location: str, limit: int) -> list[Lead]:
        leads = []
        try:
            leads = search_yelp_businesses(
                term=query,
                location=location,
                limit=limit,
                api_key=self.settings.yelp_api_key,
            )
        except Exception:
            leads = []

        if leads:
            return leads

        # Offline fallback: return a few deterministic sample leads
        return [
            Lead(
                company_name="Sample Senior Care A",
                phone="(555) 010-0001",
                address=f"{location}",
                location=location,
                website="https://example.com",
                source="mock",
                rating=4.6,
                review_count=120,
            ),
            Lead(
                company_name="Sample Nursing Home B",
                phone="(555) 010-0002",
                address=f"{location}",
                location=location,
                website="https://example.org",
                source="mock",
                rating=4.1,
                review_count=42,
            ),
        ]
