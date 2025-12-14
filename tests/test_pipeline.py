from __future__ import annotations

from pathlib import Path

from autoleadgen.config import Settings
from autoleadgen.pipeline import LeadGenerationPipeline


def test_pipeline_sequential_runs_without_keys(tmp_path: Path) -> None:
    settings = Settings(use_langgraph=False)
    pipeline = LeadGenerationPipeline(settings)

    result = pipeline.execute(
        query="nursing home",
        location="Los Angeles, CA",
        limit=5,
        enrich=False,
        qualify=True,
        generate_campaigns=True,
        output_dir=tmp_path,
    )

    assert len(result.leads) > 0
    assert len(result.enriched_leads) == len(result.leads)
    assert len(result.qualified_leads) == len(result.enriched_leads)
    assert len(result.outreach) == len(result.qualified_leads)


def test_pipeline_langgraph_runs_without_keys(tmp_path: Path) -> None:
    settings = Settings(use_langgraph=True)
    pipeline = LeadGenerationPipeline(settings)

    result = pipeline.execute(
        query="nursing home",
        location="Los Angeles, CA",
        limit=5,
        enrich=False,
        qualify=True,
        generate_campaigns=True,
        output_dir=tmp_path,
    )

    assert len(result.leads) > 0
    assert len(result.enriched_leads) == len(result.leads)
