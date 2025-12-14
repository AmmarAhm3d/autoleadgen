from __future__ import annotations

import os
import re
from typing import Any

import requests

from ..models import EnrichedLead
from ..utils import find_emails_in_text, generate_email_guesses


_FIRECRAWL_URL = "https://api.firecrawl.dev/v2/scrape"


def _simple_fetch(url: str) -> str | None:
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


def enrich_lead_contact_info(
    lead: EnrichedLead,
    *,
    api_key: str | None = None,
) -> EnrichedLead:
    """Try to enrich a lead with email/owner_name.

    - If FIRECRAWL_API_KEY is present, use Firecrawl JSON extraction.
    - Otherwise, fall back to a basic HTTP fetch + regex email extraction.
    """
    api_key = api_key or os.getenv("FIRECRAWL_API_KEY")

    website = lead.website
    if not website:
        # Nothing to scrape; keep as-is.
        return lead

    # Firecrawl path
    if api_key:
        try:
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload: dict[str, Any] = {
                "url": website,
                "onlyMainContent": False,
                "maxAge": 172800000,
                "formats": [
                    "markdown",
                    {
                        "type": "json",
                        "prompt": (
                            "Extract contact information from this business site. "
                            "Return JSON with keys: emails (array of strings), owner_name (string), phone (string)."
                        ),
                    },
                ],
            }

            resp = requests.post(_FIRECRAWL_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
            if not data.get("success"):
                return lead.model_copy(update={"enrichment_notes": f"Firecrawl unsuccessful: {data.get('error')!s}"})

            d = data.get("data") or {}
            markdown = d.get("markdown") or ""
            json_data = d.get("json") or {}

            emails: list[str] = []
            if isinstance(json_data, dict) and json_data.get("emails"):
                e = json_data.get("emails")
                if isinstance(e, list):
                    emails.extend([str(x) for x in e])
                else:
                    emails.append(str(e))
            emails.extend(find_emails_in_text(markdown))
            emails = sorted(set([e.strip() for e in emails if e and "@" in e]))

            owner_name = None
            if isinstance(json_data, dict):
                owner_name = json_data.get("owner_name") or json_data.get("owner")

            if emails and not lead.email:
                lead = lead.model_copy(update={"email": emails[0], "email_verified": True})
            if owner_name and not lead.owner_name:
                lead = lead.model_copy(update={"owner_name": str(owner_name)})

            if not lead.email:
                guesses = generate_email_guesses(website)
                if guesses:
                    lead = lead.model_copy(update={"email": guesses[0], "email_verified": False})

            return lead
        except Exception as e:
            # fall through to basic scraping
            lead = lead.model_copy(update={"enrichment_notes": f"Firecrawl failed; fallback used: {e}"})

    # Fallback path: fetch + regex emails
    html = _simple_fetch(website)
    emails = find_emails_in_text(html or "")

    if emails and not lead.email:
        return lead.model_copy(update={"email": emails[0], "email_verified": False})

    if not lead.email:
        guesses = generate_email_guesses(website)
        if guesses:
            return lead.model_copy(update={"email": guesses[0], "email_verified": False})

    return lead


_OWNER_PATTERNS = [
    re.compile(r"(?:Owner|President|CEO|Director|Manager|Administrator|Founder)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)"),
]


def guess_owner_name(text: str | None) -> str | None:
    if not text:
        return None
    for pat in _OWNER_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1).strip()
    return None
