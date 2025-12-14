from __future__ import annotations

import argparse

from autoleadgen.pipeline import LeadGenerationPipeline


def main() -> int:
    p = argparse.ArgumentParser(description="Run AutoLeadGen pipeline")
    p.add_argument("--query", required=True)
    p.add_argument("--location", required=True)
    p.add_argument("--limit", type=int, default=50)
    args = p.parse_args()

    pipeline = LeadGenerationPipeline.from_env()
    pipeline.execute(query=args.query, location=args.location, limit=args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
