from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TypedDict

from .agents import EnrichmentAgent, OutreachAgent, QualificationAgent, ScraperAgent
from .config import Settings, load_settings
from .models import EnrichedLead, Lead, PipelineResult, QualifiedLead
from .utils import dedupe_by_company_and_phone


class LeadState(TypedDict, total=False):
    query: str
    location: str
    limit: int
    leads: list[Lead]
    enriched_leads: list[EnrichedLead]
    qualified_leads: list[QualifiedLead]


@dataclass
class LeadGenerationPipeline:
    settings: Settings

    @classmethod
    def from_env(cls) -> "LeadGenerationPipeline":
        return cls(load_settings())

    def execute(
        self,
        *,
        query: str | None = None,
        location: str | None = None,
        limit: int | None = None,
        enrich: bool = True,
        qualify: bool = True,
        generate_campaigns: bool = True,
        output_dir: Path | None = None,
    ) -> PipelineResult:
        query = query or self.settings.default_query
        location = location or self.settings.default_location
        limit = limit or self.settings.default_limit

        output_dir = output_dir or self.settings.data_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        if self.settings.use_langgraph:
            result = self._execute_with_langgraph(
                query=query,
                location=location,
                limit=limit,
                enrich=enrich,
                qualify=qualify,
                generate_campaigns=generate_campaigns,
            )
        else:
            result = self._execute_sequential(
                query=query,
                location=location,
                limit=limit,
                enrich=enrich,
                qualify=qualify,
                generate_campaigns=generate_campaigns,
            )

        self._write_outputs(result, output_dir=output_dir)
        return result

    def _execute_sequential(
        self,
        *,
        query: str,
        location: str,
        limit: int,
        enrich: bool,
        qualify: bool,
        generate_campaigns: bool,
    ) -> PipelineResult:
        scraper = ScraperAgent(self.settings)
        enricher = EnrichmentAgent(self.settings)
        qualifier = QualificationAgent(self.settings)
        outreach = OutreachAgent(self.settings)

        leads = scraper.discover_leads(query=query, location=location, limit=limit)
        enriched = enricher.enrich_batch(leads) if enrich else [EnrichedLead(**l.model_dump()) for l in leads]
        enriched = dedupe_by_company_and_phone(enriched)
        qualified = qualifier.qualify(enriched) if qualify else [QualifiedLead(**e.model_dump()) for e in enriched]
        messages = outreach.generate(qualified) if generate_campaigns else []

        return PipelineResult(leads=leads, enriched_leads=enriched, qualified_leads=qualified, outreach=messages)

    def _execute_with_langgraph(
        self,
        *,
        query: str,
        location: str,
        limit: int,
        enrich: bool,
        qualify: bool,
        generate_campaigns: bool,
    ) -> PipelineResult:
        try:
            from langgraph.graph import StateGraph
        except Exception:
            # Fallback if LangGraph isn't installed.
            return self._execute_sequential(
                query=query,
                location=location,
                limit=limit,
                enrich=enrich,
                qualify=qualify,
                generate_campaigns=generate_campaigns,
            )

        scraper = ScraperAgent(self.settings)
        enricher = EnrichmentAgent(self.settings)
        qualifier = QualificationAgent(self.settings)
        outreach = OutreachAgent(self.settings)

        def scrape_node(state: LeadState) -> LeadState:
            leads = scraper.discover_leads(query=state["query"], location=state["location"], limit=state["limit"])
            return {**state, "leads": leads}

        def enrich_node(state: LeadState) -> LeadState:
            if not enrich:
                enriched_leads = [EnrichedLead(**l.model_dump()) for l in state.get("leads", [])]
            else:
                enriched_leads = enricher.enrich_batch(state.get("leads", []))
            enriched_leads = dedupe_by_company_and_phone(enriched_leads)
            return {**state, "enriched_leads": enriched_leads}

        def qualify_node(state: LeadState) -> LeadState:
            if not qualify:
                qualified_leads = [QualifiedLead(**e.model_dump()) for e in state.get("enriched_leads", [])]
            else:
                qualified_leads = qualifier.qualify(state.get("enriched_leads", []))
            return {**state, "qualified_leads": qualified_leads}

        def outreach_node(state: LeadState) -> LeadState:
            # Outreach isn't stored in LeadState to keep it simple; pipeline builds it after invoke.
            return state

        graph = StateGraph(LeadState)
        graph.add_node("scrape", scrape_node)
        graph.add_node("enrich", enrich_node)
        graph.add_node("qualify", qualify_node)
        graph.add_node("outreach", outreach_node)

        graph.set_entry_point("scrape")
        graph.add_edge("scrape", "enrich")
        graph.add_edge("enrich", "qualify")
        graph.add_edge("qualify", "outreach")

        app = graph.compile()
        final_state: LeadState = app.invoke({"query": query, "location": location, "limit": limit})

        leads = final_state.get("leads", [])
        enriched_leads = final_state.get("enriched_leads", [])
        qualified_leads = final_state.get("qualified_leads", [])

        messages = outreach.generate(qualified_leads) if generate_campaigns else []
        return PipelineResult(
            leads=leads,
            enriched_leads=enriched_leads,
            qualified_leads=qualified_leads,
            outreach=messages,
        )

    def _write_outputs(self, result: PipelineResult, *, output_dir: Path) -> None:
        ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        leads_csv = output_dir / f"leads_{ts}.csv"
        enriched_csv = output_dir / f"enriched_leads_{ts}.csv"
        qualified_csv = output_dir / f"qualified_leads_{ts}.csv"
        outreach_csv = output_dir / f"outreach_{ts}.csv"

        _write_csv(leads_csv, [l.model_dump() for l in result.leads])
        _write_csv(enriched_csv, [l.model_dump() for l in result.enriched_leads])
        _write_csv(qualified_csv, [l.model_dump() for l in result.qualified_leads])
        _write_csv(outreach_csv, [m.model_dump() for m in result.outreach])

    def crewai_smoke_test(self) -> str:
        """Small, deterministic CrewAI run to verify installation.

        This does not attempt to run the full pipeline via CrewAI (that typically
        requires a real LLM). It only verifies that CrewAI can create an agent,
        task, and kickoff successfully.
        """
        try:
            import os

            from crewai import Agent, Crew, Task
            from crewai.llms.base_llm import BaseLLM
        except Exception as e:
            return f"CrewAI not available: {e}"

        # CrewAI 1.x can prompt interactively about trace viewing on first run.
        # Mark this execution as test-like to keep the smoke test non-interactive.
        os.environ.setdefault("CREWAI_TESTING", "true")

        class DeterministicLLM(BaseLLM):
            def call(  # type: ignore[override]
                self,
                messages: str | list[dict[str, str]],
                tools=None,
                callbacks=None,
                available_functions=None,
                from_task=None,
                from_agent=None,
                response_model=None,
            ) -> str:
                return "ready"

        llm = DeterministicLLM(model="deterministic")
        agent = Agent(role="Smoke Tester", goal="Confirm CrewAI runs", backstory="CI helper", llm=llm)
        task = Task(description="Reply with the single word 'ready'.", expected_output="ready", agent=agent)
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        out = crew.kickoff()
        return str(out)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames: list[str] = sorted({k for r in rows for k in r.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
