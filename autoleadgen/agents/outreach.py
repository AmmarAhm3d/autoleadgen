from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings
from ..models import OutreachMessage, QualifiedLead


@dataclass
class OutreachAgent:
    settings: Settings

    def generate(self, leads: list[QualifiedLead]) -> list[OutreachMessage]:
        messages: list[OutreachMessage] = []
        for lead in leads:
            to_email = lead.email
            subject = f"Quick question for {lead.company_name}"
            opener = f"Hi{(' ' + lead.owner_name) if lead.owner_name else ''}," if lead.owner_name else "Hi there,"
            body = (
                f"{opener}\n\n"
                f"I’m reaching out because we work with senior care providers to help them capture more local demand "
                f"(without adding admin overhead).\n\n"
                f"If it’s useful, I can share 2–3 quick ideas tailored to {lead.company_name}. "
                f"Would you be open to a 10-minute call this week?\n\n"
                f"Best,\nAutoLeadGen"
            )
            messages.append(OutreachMessage(company_name=lead.company_name, to_email=to_email, subject=subject, body=body))
        return messages
