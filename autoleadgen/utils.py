from __future__ import annotations

import re
from typing import Iterable
from urllib.parse import urlparse

from .models import EnrichedLead, QualifiedLead


_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def extract_domain(url: str | None) -> str | None:
    if not url:
        return None
    try:
        parsed = urlparse(url if url.startswith("http") else f"https://{url}")
        host = parsed.netloc or parsed.path
        host = re.sub(r"^www\.", "", host)
        return host or None
    except Exception:
        return None


def generate_email_guesses(website: str | None) -> list[str]:
    domain = extract_domain(website)
    if not domain:
        return []
    return [
        f"info@{domain}",
        f"contact@{domain}",
        f"hello@{domain}",
        f"admin@{domain}",
    ]


def find_emails_in_text(text: str | None) -> list[str]:
    if not text:
        return []
    emails = sorted(set(_EMAIL_RE.findall(text)))
    # filter noise
    skip = ("example.com", "yourdomain", "domain.com", "email.com", "yelp.com")
    return [e for e in emails if not any(s in e.lower() for s in skip)]


def score_lead(lead: EnrichedLead) -> QualifiedLead:
    score = 0
    reasons: list[str] = []

    if lead.company_name:
        score += 25
    if lead.phone:
        score += 15
    if lead.address or lead.location:
        score += 15
    if lead.website:
        score += 10
    if lead.email:
        score += 20
        if lead.email_verified:
            score += 5
    if lead.rating is not None:
        score += min(10, int(round(lead.rating * 2)))  # 0..10
    if lead.review_count is not None:
        score += min(10, int(lead.review_count / 20))  # 0..10

    score = max(0, min(score, 100))

    if score >= 80:
        tier = "High"
    elif score >= 60:
        tier = "Medium"
    else:
        tier = "Low"

    if lead.email and lead.website:
        reasons.append("Has email + website")
    elif lead.website:
        reasons.append("Has website")
    elif lead.email:
        reasons.append("Has email")

    if lead.rating is not None:
        reasons.append(f"Rating {lead.rating}")

    return QualifiedLead(
        **lead.model_dump(),
        quality_score=score,
        tier=tier,
        qualification_reason="; ".join(reasons) or None,
    )


def dedupe_by_company_and_phone(leads: Iterable[EnrichedLead]) -> list[EnrichedLead]:
    seen_company: set[str] = set()
    seen_phone: set[str] = set()
    out: list[EnrichedLead] = []

    for lead in leads:
        company_key = (lead.company_name or "").strip().lower()
        phone_key = (lead.phone or "").strip()

        if phone_key and phone_key in seen_phone:
            continue
        if company_key and company_key in seen_company:
            continue

        if phone_key:
            seen_phone.add(phone_key)
        if company_key:
            seen_company.add(company_key)

        out.append(lead)

    return out
