# System Architecture

## Overview

AutoLeadGen is built on a multi-agent system architecture using CrewAI and LangGraph. The system orchestrates multiple specialized agents that work together to discover, enrich, qualify, and reach out to potential business leads.

## Agent Architecture

### 1. **Scraper Agent**
**Responsibility**: Discover and collect leads from multiple sources

**Capabilities**:
- Yelp Fusion API integration for business discovery
- Government directory scraping (CAHSAH, county databases)
- PDF document parsing for industry directories
- Deduplication and normalization

**Workflow**:
```
User Request → Query Definition → API/Web Calls → Data Extraction → Normalization → Output
```

### 2. **Enrichment Agent**
**Responsibility**: Extract real contact information from discovered leads

**Capabilities**:
- URL resolution (Yelp redirect → real website)
- Contact information extraction via Firecrawl
- Email address verification
- Owner/manager name extraction
- Real-time business data updates

**Workflow**:
```
Raw Leads → Playwright (URL Resolution) → Firecrawl Scraping → Data Cleaning → Enriched Leads
```

### 3. **Qualification Agent**
**Responsibility**: Score and tier leads based on quality metrics

**Capabilities**:
- Lead quality scoring (0-100)
- Tier assignment (High/Medium/Low)
- Decision-maker identification
- Business maturity assessment

**Scoring Factors**:
- Company rating (Yelp stars)
- Review count (recency & volume)
- Email verification status
- Contact information completeness
- Industry classification

### 4. **Outreach Agent**
**Responsibility**: Manage lead outreach campaigns

**Capabilities**:
- Personalized email template generation
- Multi-touch campaign sequencing
- A/B testing framework
- Response tracking
- Follow-up automation

## Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      DATA INGESTION LAYER                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Yelp API    │  Government    │  PDF          │  Custom         │
│   Integration │  Directories   │  Scraping     │  Sources        │
│               │                │               │                 │
└─────────┬──────────────────────────────────────────────────────┬─┘
          │                                                      │
          ▼                                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                    NORMALIZATION & DEDUP LAYER                   │
├──────────────────────────────────────────────────────────────────┤
│  • Standard field mapping                                         │
│  • Duplicate detection (by business ID, phone, address)          │
│  • Data quality validation                                       │
│  • Outlier detection                                             │
└──────────────┬─────────────────────────────────────────────────┬─┘
               │                                                 │
               ▼                                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                   ENRICHMENT LAYER (Firecrawl)                   │
├──────────────────────────────────────────────────────────────────┤
│  • URL Resolution                  │  • Contact Extraction       │
│  • Website Scraping                │  • Email Verification       │
│  • Content Analysis                │  • Owner/Manager Detection   │
└──────────────┬─────────────────────────────────────────────────┬─┘
               │                                                 │
               ▼                                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                  QUALIFICATION & SCORING LAYER                   │
├──────────────────────────────────────────────────────────────────┤
│  • Lead Quality Score (ML-based)                                 │
│  • Tier Classification (High/Medium/Low)                         │
│  • Decision-Maker Identification                                 │
│  • Business Classification                                       │
└──────────────┬─────────────────────────────────────────────────┬─┘
               │                                                 │
               ▼                                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STORAGE & RETRIEVAL LAYER                     │
├──────────────────────────────────────────────────────────────────┤
│  SQLite Database                                                 │
│  ├── leads (id, company_name, industry, created_at)            │
│  ├── contacts (id, lead_id, email, phone, owner_name)          │
│  ├── scores (id, lead_id, quality_score, tier, reason)         │
│  └── campaigns (id, lead_id, status, sent_at, response_at)     │
└──────────────┬─────────────────────────────────────────────────┬─┘
               │                                                 │
               ▼                                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    OUTREACH ORCHESTRATION LAYER                  │
├──────────────────────────────────────────────────────────────────┤
│  • Email Campaign Generation                                     │
│  • Personalization Engine (via RAG)                              │
│  • Multi-touch Sequencing                                       │
│  • Conversion Tracking                                          │
└──────────────────────────────────────────────────────────────────┘
```

## CrewAI Integration

### Agent Definition Example
```python
from crewai import Agent, Task, Crew

scraper_agent = Agent(
    role="Lead Discovery Specialist",
    goal="Discover high-quality business leads from multiple sources",
    backstory="Expert in business databases and web research",
    tools=[yelp_search, directory_scraper, pdf_parser],
    llm=claude_llm,
    verbose=True
)

scraping_task = Task(
    description="Search for nursing home services in Southern California",
    agent=scraper_agent,
    expected_output="CSV with 100+ business leads",
)

crew = Crew(
    agents=[scraper_agent, enrichment_agent, qualification_agent, outreach_agent],
    tasks=[scraping_task, enrichment_task, qualification_task, outreach_task],
    process=Process.sequential,
    verbose=True
)
```

## LangGraph Implementation

LangGraph manages complex agent workflows and state transitions:

```python
from langgraph.graph import StateGraph

workflow = StateGraph(AgentState)

# Add nodes for each agent
workflow.add_node("scraper", scraper_node)
workflow.add_node("enrichment", enrichment_node)
workflow.add_node("qualification", qualification_node)
workflow.add_node("outreach", outreach_node)

# Define edges (workflow routing)
workflow.add_edge("scraper", "enrichment")
workflow.add_edge("enrichment", "qualification")
workflow.add_edge("qualification", "outreach")

# Compile and execute
app = workflow.compile()
result = app.invoke({"query": "Find nursing home leads in CA"})
```

## API Integration Points

### Yelp Fusion API
- **Endpoint**: `https://api.yelp.com/v3/businesses/search`
- **Rate Limit**: 5,000 calls/day (free tier)
- **Use Case**: Business discovery, ratings, metadata

### Firecrawl API
- **Endpoint**: `https://api.firecrawl.dev/v2/scrape`
- **Use Case**: Website scraping, structured extraction
- **Schema**: JSON extraction for contact information

### Playwright
- **Use Case**: Dynamic URL resolution, JavaScript rendering
- **Feature**: Yelp redirect URL → actual business website

## Error Handling & Resilience

### Retry Logic
```python
@retry(max_attempts=3, backoff_factor=2)
def api_call_with_retry():
    # Exponential backoff: 1s, 2s, 4s
    pass
```

### Rate Limiting
```python
limiter = RateLimiter(calls_per_minute=100)
for lead in leads:
    limiter.wait()
    process_lead(lead)
```

### Graceful Degradation
- If Firecrawl fails → use fallback email patterns
- If Yelp URL unavailable → generate inferred email
- If owner name not found → skip personalization

## Performance Optimization

### Parallel Processing
```python
# Process multiple leads concurrently
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(enrich_lead, lead) for lead in leads]
    enriched = [f.result() for f in futures]
```

### Caching Strategy
- Cache Yelp API responses (24 hours)
- Cache website content from Firecrawl (48 hours)
- In-memory deduplication cache

### Database Indexing
```sql
CREATE INDEX idx_company_phone ON leads(phone);
CREATE INDEX idx_email ON contacts(email);
CREATE INDEX idx_lead_quality_score ON scores(quality_score DESC);
```

## Monitoring & Logging

### Key Metrics
- **Leads discovered**: Count per source
- **Enrichment rate**: % of leads with real emails
- **Processing time**: Avg time per lead
- **API costs**: Cost per lead
- **Error rate**: Failed requests %

### Logging Levels
- **DEBUG**: Detailed API calls, all operations
- **INFO**: Pipeline milestones, lead counts
- **WARNING**: Failed enrichments, missing data
- **ERROR**: API failures, critical issues

## Scalability Considerations

### Horizontal Scaling
- Distribute agents across multiple machines
- Use task queues (Celery/RQ) for job distribution
- Database sharding for large lead volumes

### Vertical Scaling
- Increase Firecrawl concurrency
- Higher Yelp API rate limits
- GPU acceleration for ML-based scoring

### Cost Optimization
- Use caching to reduce API calls
- Batch processing to minimize requests
- Free tier APIs where possible

---

**Last Updated**: December 2025
