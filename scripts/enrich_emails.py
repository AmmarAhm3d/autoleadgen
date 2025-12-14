from __future__ import annotations

import argparse
import pandas as pd

from autoleadgen.config import load_settings
from autoleadgen.models import EnrichedLead
from autoleadgen.tools.firecrawl import enrich_lead_contact_info


def main() -> int:
    p = argparse.ArgumentParser(description="Enrich a CSV of leads with emails")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max", type=int, default=50)
    args = p.parse_args()

    settings = load_settings()
    df = pd.read_csv(args.input)
    df = df.head(args.max)

    out_rows = []
    for _, row in df.iterrows():
        lead = EnrichedLead(**{k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()})
        out_rows.append(enrich_lead_contact_info(lead, api_key=settings.firecrawl_api_key).model_dump())

    pd.DataFrame(out_rows).to_csv(args.output, index=False)
    print(f"Wrote {len(out_rows)} enriched leads to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
