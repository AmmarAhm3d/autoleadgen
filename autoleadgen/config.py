from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    # API keys
    yelp_api_key: str | None = None
    firecrawl_api_key: str | None = None
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    groq_api_key: str | None = None

    # LLM configuration
    groq_model: str = "llama-3.1-8b-instant"
    outreach_llm: str = "template"  # 'template' | 'groq'

    # defaults
    default_query: str = "nursing home"
    default_location: str = "Los Angeles, CA"
    default_limit: int = 25

    # execution
    use_langgraph: bool = True

    # IO
    project_root: Path = Path(__file__).resolve().parents[1]

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data"

    @property
    def logs_dir(self) -> Path:
        return self.project_root / "logs"


def load_settings() -> Settings:
    """Load settings from environment.

    If python-dotenv is installed, this will also load a .env file from the
    project root when present.
    """
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env", override=False)
    except Exception:
        # Optional dependency / best-effort.
        pass

    def _get_bool(name: str, default: bool) -> bool:
        raw = os.getenv(name)
        if raw is None:
            return default
        return raw.strip().lower() in {"1", "true", "yes", "y"}

    def _get_int(name: str, default: int) -> int:
        raw = os.getenv(name)
        if raw is None:
            return default
        try:
            return int(raw)
        except ValueError:
            return default

    return Settings(
        yelp_api_key=os.getenv("YELP_API_KEY"),
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        outreach_llm=os.getenv("OUTREACH_LLM", "template"),
        default_query=os.getenv("DEFAULT_QUERY", "nursing home"),
        default_location=os.getenv("DEFAULT_LOCATION", "Los Angeles, CA"),
        default_limit=_get_int("DEFAULT_LIMIT", 25),
        use_langgraph=_get_bool("USE_LANGGRAPH", True),
    )
