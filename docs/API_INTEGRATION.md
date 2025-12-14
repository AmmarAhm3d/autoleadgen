# API Integration Guide

Complete guide to setting up and using all third-party APIs in AutoLeadGen.

## 📋 Table of Contents

1. [Yelp Fusion API](#yelp-fusion-api)
2. [Firecrawl API](#firecrawl-api)
3. [Anthropic Claude API](#anthropic-claude-api)
4. [OpenAI API (Optional)](#openai-api-optional)
5. [Groq API (Optional)](#groq-api-optional)
6. [Environment Configuration](#environment-configuration)
7. [Testing Connections](#testing-connections)
8. [Rate Limiting & Quotas](#rate-limiting--quotas)
9. [Error Handling](#error-handling)

---

## 🍋 Yelp Fusion API

### Overview
Yelp Fusion API provides access to business data including:
- Business discovery by category, location, search term
- Business details (ratings, reviews, photos)
- Business search rankings
- Review retrieval

### Setup

#### 1. Create App Registration
1. Go to [Yelp Developers](https://www.yelp.com/developers)
2. Click "Create New App"
3. Fill in app details:
   - **App Name**: `AutoLeadGen`
   - **App Description**: Autonomous lead generation system
   - **Website**: (optional)
4. Accept terms and create

#### 2. Get API Key
- Find your **API Key** on the app management page
- Add to `.env`:
```env
YELP_API_KEY=your_api_key_here
```

### Usage Examples

#### Basic Business Search
```python
from autoleadgen.tools import YelpSearcher

searcher = YelpSearcher(api_key=os.getenv("YELP_API_KEY"))

# Search for businesses
results = searcher.search(
    term="nursing home",
    location="Los Angeles, CA",
    limit=50,
    sort_by="rating"
)

for business in results:
    print(f"{business['name']} - {business['rating']} stars")
```

#### Get Business Details
```python
# Get detailed info on specific business
business = searcher.get_business(business_id)

print(f"Name: {business['name']}")
print(f"Rating: {business['rating']}")
print(f"Reviews: {business['review_count']}")
print(f"Phone: {business['phone']}")
print(f"Address: {business['location']['display_address']}")
```

#### Search with Filters
results = searcher.search(
    location="Los Angeles",
    categories="healthserv",
    attributes="open_now",
    price="$$",
    sort_by="review_count",
    limit=100
)
```

### Rate Limits
- **Free Tier**: 5,000 API calls/day
- **Paid Tier**: Higher limits available
- **Pricing**: Free for basic searches

### Common Categories
```
healthserv    - Health Services
hospitals     - Hospitals
homehealthcare - Home Health Care
seniorcare    - Senior Care
hospice       - Hospice Services
```

### Endpoint Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v3/businesses/search` | GET | Search businesses |
| `/v3/businesses/{id}` | GET | Get business details |
| `/v3/businesses/{id}/reviews` | GET | Get business reviews |
| `/v3/autocomplete` | GET | Search autocomplete |

---

## 🔥 Firecrawl API

### Overview
Firecrawl provides intelligent web scraping and structured data extraction:
- Convert websites to clean, parseable content (markdown)
- Extract structured data from web pages
- Screenshot capture
- Batch scraping

### Setup

#### 1. Create Account
1. Go to [Firecrawl Dashboard](https://app.firecrawl.dev)
2. Sign up for account
3. Create new project

#### 2. Get API Key
- Find your API Key in account settings
- Add to `.env`:
```env
FIRECRAWL_API_KEY=your_api_key_here
```

### Usage Examples

#### Basic Web Scraping
```python
from autoleadgen.tools import FirecrawlClient

client = FirecrawlClient(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Scrape website to markdown
result = client.scrape(
    url="https://example.com",
    format="markdown"
)

print(result['markdown'])
```

#### Extract Structured Data
```python
# Extract specific fields as JSON
result = client.extract(
    url="https://example.com",
    schema={
        "type": "object",
        "properties": {
            "company_name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "owner": {"type": "string"}
        },
        "required": ["company_name", "email"]
    }
)

print(result['data'])
# Output: {
#   "company_name": "ABC Nursing Home",
#   "email": "contact@abc.com",
#   "phone": "555-123-4567",
#   "owner": "John Smith"
# }
```

#### Screenshot Capture
```python
# Capture website screenshot
result = client.scrape(
    url="https://example.com",
    format="screenshot",
    screenshot_options={
        "width": 1920,
        "height": 1080,
        "fullPage": True
    }
)

# Save screenshot
with open("screenshot.png", "wb") as f:
    f.write(result['screenshot'])
```

#### Batch Scraping
```python
# Scrape multiple URLs concurrently
urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
]

results = client.batch_scrape(urls, concurrency=5)

for url, data in zip(urls, results):
    print(f"{url}: {len(data['markdown'])} chars")
```

### Rate Limits
- **Free Tier**: 100 scrapes/month
- **Pro Tier**: 500 scrapes/month
- **Enterprise**: Custom limits
- **Rate**: 10 concurrent requests max

### Configuration Options

```python
client.scrape(
    url="https://example.com",
    format="markdown",          # markdown, html, screenshot, json
    exclude_tags=["script", "style"],  # Exclude tags
    include_tags=["body"],      # Include only tags
    wait_for=5000,              # Wait for JS (ms)
    timeout=30000,              # Request timeout (ms)
    mobile=False,               # Mobile user agent
    cache=True                  # Use cached results
)
```

---

## 🤖 Anthropic Claude API

### Overview
Claude API for intelligent text generation:
- Lead qualification and scoring
- Email personalization
- Campaign generation
- Content analysis

### Setup

#### 1. Create Account
1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up for account
3. Create new API key

#### 2. Add API Key
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### Usage Examples

#### Basic Message
```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "What is AutoLeadGen?"
        }
    ]
)

print(message.content[0].text)
```

#### Email Generation with Context
```python
# Generate personalized email
email_prompt = f"""
Generate a professional outreach email for:
- Company: {company_name}
- Industry: {industry}
- Decision Maker: {owner_name}
- Business Focus: {business_description}

Email should:
1. Personalize with company/owner name
2. Show understanding of their business
3. Offer clear value proposition
4. Include call-to-action
5. Keep under 200 words

Return ONLY the email body.
"""

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    messages=[{"role": "user", "content": email_prompt}]
)

email_body = message.content[0].text
```

#### Lead Scoring
```python
# Score lead quality
scoring_prompt = f"""
Score the quality of this business lead:
- Company: {company_name}
- Rating: {yelp_rating}
- Reviews: {review_count}
- Email Verified: {email_verified}
- Owner Identified: {owner_identified}

Provide:
1. Quality score (0-100)
2. Tier (High/Medium/Low)
3. Key strengths
4. Risk factors
5. Recommended action

Format as JSON.
"""

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    messages=[{"role": "user", "content": scoring_prompt}]
)

# Parse JSON response
import json
result = json.loads(message.content[0].text)
```

### Model Selection

| Model | Speed | Cost | Recommended Use |
|-------|-------|------|-----------------|
| claude-3-5-sonnet | Fast | Low | Emails, classification |
| claude-3-opus | Slow | High | Complex reasoning |
| claude-3-haiku | Very Fast | Very Low | Simple tasks |

### Pricing
- **Input**: $3 per 1M tokens
- **Output**: $15 per 1M tokens
- Free trial with $5 credit

---

## 🧠 OpenAI API (Optional)

### Overview
For embeddings and advanced language processing:
- Text embeddings for RAG
- Additional NLP tasks

### Setup

```bash
pip install openai
```

```env
OPENAI_API_KEY=your_api_key_here
```

### Usage

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="nursing home in Los Angeles"
)

embedding = response.data[0].embedding
print(f"Embedding dimension: {len(embedding)}")
```

---

## 🥭 Groq API (Optional)

### Overview
AutoLeadGen can optionally use Groq to generate outreach emails via Groq's OpenAI-compatible chat completions endpoint.

### Setup
Add to `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
OUTREACH_LLM=groq
```

### Usage
Run the pipeline with Groq-powered outreach:
```bash
autoleadgen --outreach-llm groq
```

To keep deterministic template outreach:
```bash
autoleadgen --outreach-llm template
```

---

## ⚙️ Environment Configuration

### Complete .env Template

```env
# ============================================================================
# AutoLeadGen Configuration
# ============================================================================

# REQUIRED: API Keys
# ────────────────────────────────────────────────────────────────────────

# Yelp Fusion API - Business discovery
# Get from: https://www.yelp.com/developers
YELP_API_KEY=your_yelp_api_key_here

# Firecrawl API - Web scraping & extraction
# Get from: https://app.firecrawl.dev
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Anthropic Claude - LLM for AI tasks
# Get from: https://console.anthropic.com
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI - Embeddings and NLP (optional)
# Get from: https://platform.openai.com
OPENAI_API_KEY=your_openai_api_key_here

# Groq - Outreach generation (optional)
# Get from: https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
OUTREACH_LLM=template  # set to 'groq' to enable Groq outreach

# DATABASE
# ────────────────────────────────────────────────────────────────────────
DATABASE_URL=sqlite:///./leads.db
DATABASE_ECHO=False  # Set to True to see SQL queries

# LOGGING
# ────────────────────────────────────────────────────────────────────────
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/autoleadgen.log
LOG_MAX_SIZE=10485760  # 10MB

# RATE LIMITING & PERFORMANCE
# ────────────────────────────────────────────────────────────────────────
FIRECRAWL_CONCURRENCY=5
FIRECRAWL_TIMEOUT=30
YELP_RATE_LIMIT=100  # requests per minute
PLAYWRIGHT_TIMEOUT=30000  # ms

# FIRECRAWL SETTINGS
# ────────────────────────────────────────────────────────────────────────
FIRECRAWL_FORMAT=markdown  # markdown, html, screenshot
FIRECRAWL_USE_CACHE=True
FIRECRAWL_CACHE_TTL=172800  # 48 hours in seconds

# SCRAPING SETTINGS
# ────────────────────────────────────────────────────────────────────────
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
SCRAPER_TIMEOUT=30
USE_PROXY=False
PROXY_FILE=data/proxies.txt

# EMAIL SETTINGS
# ────────────────────────────────────────────────────────────────────────
EMAIL_VERIFICATION_ENABLED=True
EMAIL_PROVIDER=mailmodo  # mailmodo, zeroBounce, hunter
EMAIL_VERIFICATION_API_KEY=your_email_verification_key

# FEATURE FLAGS
# ────────────────────────────────────────────────────────────────────────
ENABLE_EMAIL_ENRICHMENT=True
ENABLE_OWNER_DETECTION=True
ENABLE_PDF_PARSING=False
ENABLE_BATCH_PROCESSING=True

# DEVELOPMENT
# ────────────────────────────────────────────────────────────────────────
DEBUG=False
TESTING=False
ALLOW_EXTERNAL_LINKS=False
```

### Loading Configuration

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
yelp_api_key = os.getenv("YELP_API_KEY")
firecrawl_key = os.getenv("FIRECRAWL_API_KEY")

# With default fallback
log_level = os.getenv("LOG_LEVEL", "INFO")
```

---

## 🧪 Testing Connections

### Test All APIs

```python
from autoleadgen.tools import test_connections

# Run all connection tests
results = test_connections()

# Output:
# {
#   "yelp": {"status": "connected", "remaining_calls": 4999},
#   "firecrawl": {"status": "connected", "plan": "pro"},
#   "claude": {"status": "connected", "model": "claude-3-5-sonnet"},
#   "openai": {"status": "connected", "organization": "your-org"}
# }
```

### Test Individual APIs

```python
# Test Yelp
from autoleadgen.tools import YelpSearcher
searcher = YelpSearcher()
status = searcher.test_connection()
print(f"Yelp: {status}")

# Test Firecrawl
from autoleadgen.tools import FirecrawlClient
client = FirecrawlClient()
status = client.test_connection()
print(f"Firecrawl: {status}")

# Test Claude
import anthropic
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=10,
    messages=[{"role": "user", "content": "Hi"}]
)
print("Claude: connected")
```

---

## 🚦 Rate Limiting & Quotas

### Yelp Fusion Limits
```
Free Tier:
- 5,000 API calls/day
- 1 request/sec
```

**Handling limits:**
```python
from autoleadgen.tools import RateLimiter

limiter = RateLimiter(requests_per_second=1)

for lead in leads:
    limiter.wait()
    result = searcher.get_business(lead['id'])
```

### Firecrawl Limits
```
Free: 100 scrapes/month
Pro: 500 scrapes/month
Enterprise: Custom
Concurrent: 10 max
```

**Handling limits:**
```python
from concurrent.futures import ThreadPoolExecutor

# Limit concurrent requests
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(scrape_url, url) for url in urls]
    results = [f.result() for f in futures]
```

### Monitoring Usage

```python
# Check remaining quota
from autoleadgen.tools import QuotaChecker

checker = QuotaChecker()

yelp_quota = checker.get_yelp_quota()
print(f"Yelp remaining: {yelp_quota['remaining']} / {yelp_quota['daily_limit']}")

firecrawl_quota = checker.get_firecrawl_quota()
print(f"Firecrawl remaining: {firecrawl_quota['remaining']}")
```

---

## ⚠️ Error Handling

### Common Errors & Solutions

#### Invalid API Key
```python
try:
    result = searcher.search(term="test")
except AuthenticationError:
    print("Invalid API key")
    # Fix: Update YELP_API_KEY in .env
```

#### Rate Limit Exceeded
```python
try:
    result = client.scrape(url)
except RateLimitError:
    print("Rate limit exceeded, retrying in 60 seconds")
    import time
    time.sleep(60)
    result = client.scrape(url)
```

#### Network Timeout
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def scrape_with_retry(url):
    return client.scrape(url)
```

### Structured Error Handling

```python
from autoleadgen.errors import (
    APIError,
    RateLimitError,
    AuthenticationError,
    TimeoutError
)

try:
    results = scraper.discover_leads(query, location)
except AuthenticationError as e:
    logger.error(f"Auth failed: {e}")
except RateLimitError as e:
    logger.warning(f"Rate limited: {e}")
    # Implement backoff
except TimeoutError as e:
    logger.error(f"Timeout: {e}")
    # Retry or skip
except APIError as e:
    logger.error(f"API error: {e}")
    # Handle gracefully
```

---

## 🎓 Examples Repository

Real-world examples:

```bash
# Yelp search
python examples/yelp_search_example.py

# Firecrawl enrichment
python examples/firecrawl_enrichment_example.py

# Email generation
python examples/email_generation_example.py

# Full pipeline
python examples/full_pipeline_example.py
```

---

**Last Updated**: December 2025
