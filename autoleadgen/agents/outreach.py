from __future__ import annotations

import json
from dataclasses import dataclass

from ..config import Settings
from ..models import OutreachMessage, QualifiedLead
from ..llms import GroqChat


@dataclass
class OutreachAgent:
    settings: Settings

    def generate(self, leads: list[QualifiedLead]) -> list[OutreachMessage]:
        use_groq = (self.settings.outreach_llm or "template").strip().lower() == "groq"
        groq = None
        if use_groq:
            if not self.settings.groq_api_key:
                raise RuntimeError("OUTREACH_LLM=groq requires GROQ_API_KEY to be set")
            groq = GroqChat(api_key=self.settings.groq_api_key, model=self.settings.groq_model)

        messages: list[OutreachMessage] = []
        for lead in leads:
            to_email = lead.email
            if groq is None:
                subject = f"Quick question for {lead.company_name}"
                opener = (
                    f"Hi{(' ' + lead.owner_name) if lead.owner_name else ''}," if lead.owner_name else "Hi there,"
                )
                body = (
                    f"{opener}\n\n"
                    f"I’m reaching out because we work with senior care providers to help them capture more local demand "
                    f"(without adding admin overhead).\n\n"
                    f"If it’s useful, I can share 2–3 quick ideas tailored to {lead.company_name}. "
                    f"Would you be open to a 10-minute call this week?\n\n"
                    f"Best,\nAutoLeadGen"
                )
            else:
                system = (
                    "You write concise, professional B2B cold emails. "
                    "Return JSON only with keys: subject, body. The body must be plain text with line breaks. "
                    "Do not include markdown."
                )
                user = (
                    "Write a short outreach email to a senior care provider.\n"
                    f"Company: {lead.company_name}\n"
                    f"Owner/Contact name (optional): {lead.owner_name or ''}\n"
                    f"Location: {lead.location or ''}\n"
                    "Goal: ask for a 10-minute call this week.\n"
                    "Tone: friendly, direct, respectful.\n"
                )
                raw = groq.complete(system=system, user=user, temperature=0.2)
                try:
                    parsed = json.loads(raw)
                    subject = str(parsed.get("subject") or f"Quick question for {lead.company_name}").strip()
                    body = str(parsed.get("body") or "").strip()
                    if not body:
                        raise ValueError("empty body")
                except Exception:
                    subject = f"Quick question for {lead.company_name}"
                    body = raw.strip()[:4000]

            messages.append(OutreachMessage(company_name=lead.company_name, to_email=to_email, subject=subject, body=body))
        return messages
