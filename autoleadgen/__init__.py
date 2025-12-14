"""AutoLeadGen package.

This repo includes a minimal, runnable implementation of the multi-step lead
pipeline (scrape -> enrich -> qualify -> outreach) with optional LangGraph and
CrewAI integration.
"""

from .pipeline import LeadGenerationPipeline  # noqa: F401
