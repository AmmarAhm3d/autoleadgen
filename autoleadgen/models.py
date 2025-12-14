from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Lead(BaseModel):
    company_name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    location: str | None = None
    website: str | None = None
    yelp_url: str | None = None

    rating: float | None = None
    review_count: int | None = None

    source: str = "unknown"


class EnrichedLead(Lead):
    owner_name: str | None = None
    email_verified: bool = False
    enrichment_notes: str | None = None


class QualifiedLead(EnrichedLead):
    quality_score: int = Field(ge=0, le=100, default=0)
    tier: Literal["High", "Medium", "Low"] = "Low"
    qualification_reason: str | None = None


class OutreachMessage(BaseModel):
    company_name: str
    to_email: str | None = None
    subject: str
    body: str


class PipelineResult(BaseModel):
    leads: list[Lead]
    enriched_leads: list[EnrichedLead]
    qualified_leads: list[QualifiedLead]
    outreach: list[OutreachMessage]
