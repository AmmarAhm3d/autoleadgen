from __future__ import annotations

import os
from typing import Any

import requests

from ..models import Lead


_API_HOST = "https://api.yelp.com"
_SEARCH_PATH = "/v3/businesses/search"


def search_yelp_businesses(
    *,
    term: str,
    location: str,
    limit: int,
    api_key: str | None = None,
) -> list[Lead]:
    api_key = api_key or os.getenv("YELP_API_KEY")
    if not api_key:
        return []

    url = f"{_API_HOST}{_SEARCH_PATH}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"term": term, "location": location, "limit": max(1, min(limit, 50))}

    resp = requests.get(url, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    payload: dict[str, Any] = resp.json()

    leads: list[Lead] = []
    for biz in payload.get("businesses", []) or []:
        loc = biz.get("location") or {}
        display_addr = loc.get("display_address") or []
        address = ", ".join(display_addr) if isinstance(display_addr, list) else None

        leads.append(
            Lead(
                company_name=biz.get("name") or "",
                phone=biz.get("display_phone") or biz.get("phone"),
                address=address,
                location=location,
                website=None,  # Yelp search doesn't provide business website.
                yelp_url=biz.get("url"),
                rating=biz.get("rating"),
                review_count=biz.get("review_count"),
                source="yelp",
            )
        )

    return [l for l in leads if l.company_name]
