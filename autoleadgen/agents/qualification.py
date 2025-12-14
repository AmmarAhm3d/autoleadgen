from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings
from ..models import EnrichedLead, QualifiedLead
from ..utils import score_lead


@dataclass
class QualificationAgent:
    settings: Settings

    def qualify(self, leads: list[EnrichedLead]) -> list[QualifiedLead]:
        return [score_lead(l) for l in leads]
