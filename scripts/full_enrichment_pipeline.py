"""Convenience wrapper.

This script exists to mirror the docs/README entry points. The core pipeline
lives in autoleadgen.pipeline.
"""

from __future__ import annotations

from autoleadgen.pipeline import LeadGenerationPipeline


def main() -> int:
    pipeline = LeadGenerationPipeline.from_env()
    pipeline.execute()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
