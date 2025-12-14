from __future__ import annotations

import argparse
import json
from dataclasses import replace

from .pipeline import LeadGenerationPipeline


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AutoLeadGen CLI")
    p.add_argument("--query", default=None, help="Search query (e.g. 'nursing home')")
    p.add_argument("--location", default=None, help="Location (e.g. 'Los Angeles, CA')")
    p.add_argument("--limit", type=int, default=None, help="Max results")

    p.add_argument("--no-enrich", action="store_true", help="Skip enrichment")
    p.add_argument("--no-qualify", action="store_true", help="Skip qualification")
    p.add_argument("--no-outreach", action="store_true", help="Skip outreach generation")

    p.add_argument("--no-langgraph", action="store_true", help="Disable LangGraph execution")
    p.add_argument(
        "--outreach-llm",
        choices=["template", "groq"],
        default=None,
        help="Outreach generator to use (default: from OUTREACH_LLM env var, else template)",
    )
    p.add_argument(
        "--groq-model",
        default=None,
        help="Groq model to use when --outreach-llm groq (or GROQ_MODEL env var)",
    )
    p.add_argument("--crewai-smoke", action="store_true", help="Run CrewAI smoke test and exit")
    p.add_argument("--json", action="store_true", help="Print result summary as JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    pipeline = LeadGenerationPipeline.from_env()
    if args.no_langgraph:
        pipeline.settings = replace(pipeline.settings, use_langgraph=False)

    if args.outreach_llm is not None:
        pipeline.settings = replace(pipeline.settings, outreach_llm=args.outreach_llm)

    if args.groq_model is not None:
        pipeline.settings = replace(pipeline.settings, groq_model=args.groq_model)

    if args.crewai_smoke:
        print(pipeline.crewai_smoke_test())
        return 0

    result = pipeline.execute(
        query=args.query,
        location=args.location,
        limit=args.limit,
        enrich=not args.no_enrich,
        qualify=not args.no_qualify,
        generate_campaigns=not args.no_outreach,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "leads": len(result.leads),
                    "enriched_leads": len(result.enriched_leads),
                    "qualified_leads": len(result.qualified_leads),
                    "outreach": len(result.outreach),
                },
                indent=2,
            )
        )
    else:
        print(f"Leads: {len(result.leads)}")
        print(f"Enriched: {len(result.enriched_leads)}")
        print(f"Qualified: {len(result.qualified_leads)}")
        print(f"Outreach messages: {len(result.outreach)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
