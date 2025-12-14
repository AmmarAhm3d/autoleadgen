from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings
from ..models import EnrichedLead, Lead
from ..tools.firecrawl import enrich_lead_contact_info


@dataclass
class EnrichmentAgent:
    settings: Settings

    def enrich_batch(self, leads: list[Lead]) -> list[EnrichedLead]:
        enriched: list[EnrichedLead] = []

        for lead in leads:
            e = EnrichedLead(**lead.model_dump())
            # If website missing, keep as-is.
            if e.website:
                e = enrich_lead_contact_info(e, api_key=self.settings.firecrawl_api_key)
            enriched.append(e)

        return enriched
