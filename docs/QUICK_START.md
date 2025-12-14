# Quick Start Guide - AutoLeadGen

Get up and running with AutoLeadGen in **5 minutes**.

## 🎯 Prerequisites

- Python 3.10+
- pip/conda
- API Keys:
  - [Yelp Fusion API](https://www.yelp.com/developers)
  - [Firecrawl API](https://www.firecrawl.dev)
  - [Anthropic Claude API](https://www.anthropic.com)

## 📦 Step 1: Install

```bash
# Clone repository
git clone https://github.com/AmmarAhm3d/autoleadgen.git
cd autoleadgen

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize Playwright browsers
playwright install chromium
```

## ⚙️ Step 2: Configure

Create a `.env` file in the project root:

```env
# Required API Keys
YELP_API_KEY=your_yelp_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_key_here
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_key_here

# Optional Settings
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./leads.db
FIRECRAWL_CONCURRENCY=5
```

## 🚀 Step 3: Run Your First Campaign

### Option A: Command Line

```bash
# Discover leads from Yelp
python scripts/scrape_example.py \
  --query "nursing home services" \
  --location "Los Angeles, CA" \
  --limit 50

# Enrich with contact information
python scripts/enrich_emails.py \
  --input ./data/leads.csv \
  --output ./data/enriched_leads.csv

# Generate personalized campaigns
python scripts/generate_campaigns.py \
  --input ./data/enriched_leads.csv \
  --template "nurture_sequence"
```

### Option B: Python Script

```python
from autoleadgen.pipeline import LeadGenerationPipeline

# Initialize pipeline
pipeline = LeadGenerationPipeline()

# Run complete workflow
results = pipeline.execute(
    query="nursing home services",
    location="Los Angeles, CA",
    limit=50,
    enrich=True,
    qualify=True,
    generate_campaigns=True
)

# Access results
print(f"Leads discovered: {len(results['leads'])}")
print(f"Enriched contacts: {len(results['enriched_leads'])}")
print(f"High-tier leads: {len(results['qualified_leads']['high'])}")
```

## 📊 Step 4: View Results

Results are stored in SQLite database and exported CSVs:

```bash
# View leads
sqlite3 leads.db "SELECT * FROM leads LIMIT 10;"

# Export to CSV
python scripts/export_results.py --output results.csv

# View in notebook
jupyter notebook notebooks/01_lead_analysis.ipynb
```

## 🔍 Step 5: Monitor & Optimize

### Check Logs

```bash
# View real-time logs
tail -f logs/autoleadgen.log

# Filter by level
grep "ERROR" logs/autoleadgen.log
```

### View Database Stats

```bash
# Total leads by source
sqlite3 leads.db \
  "SELECT source, COUNT(*) FROM leads GROUP BY source;"

# Email extraction success rate
sqlite3 leads.db \
  "SELECT SUM(CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) 
   FROM contacts;"
```

## 💡 Common Use Cases

### Use Case 1: Find Nursing Home Leads in SoCal

```python
from autoleadgen.agents import ScraperAgent

scraper = ScraperAgent()
leads = scraper.discover_leads(
    query="nursing home",
    location="Southern California",
    limit=100
)
```

### Use Case 2: Enrich with Real Emails

```python
from autoleadgen.agents import EnrichmentAgent

enricher = EnrichmentAgent()
enriched = enricher.enrich_batch(leads)
# Returns: email, owner_name, website, phone
```

### Use Case 3: Score & Tier Leads

```python
from autoleadgen.agents import QualificationAgent

qualifier = QualificationAgent()
scored = qualifier.score_leads(enriched)
# Returns: quality_score (0-100), tier (High/Med/Low)
```

### Use Case 4: Generate Campaigns

```python
from autoleadgen.agents import OutreachAgent

outreach = OutreachAgent()
campaigns = outreach.generate_campaigns(
    leads=scored,
    template="nursing_home_outreach",
    personalize=True
)
```

## 🐛 Troubleshooting

### "API Key Error"
```bash
# Check .env file is in project root
cat .env | grep YELP_API_KEY

# Reload environment
export $(cat .env | xargs)
```

### "Firecrawl Rate Limit"
```python
# Reduce concurrency in config
FIRECRAWL_CONCURRENCY=2  # Was: 5

# Or batch process
from autoleadgen.tools import batch_enrich
enriched = batch_enrich(leads, batch_size=10)
```

### "Database Locked"
```bash
# Close other connections
pkill -f "sqlite3"

# Or use WAL mode
sqlite3 leads.db "PRAGMA journal_mode=WAL;"
```

### "No Leads Found"
```python
# Check Yelp API is working
from autoleadgen.tools import test_yelp_connection
test_yelp_connection()

# Try broader search
leads = scraper.discover_leads(
    query="senior care",  # More general
    location="California",  # Larger area
    limit=200
)
```

## 📚 Next Steps

1. **Customize Templates**: Edit email templates in `src/templates/`
2. **Add Data Sources**: Extend scraper with new APIs in `src/tools/`
3. **Fine-tune Scoring**: Adjust weights in `src/agents/qualification_agent.py`
4. **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Monitor Performance**: Check [ARCHITECTURE.md](ARCHITECTURE.md#monitoring--logging)

## 📖 Full Documentation

- [System Architecture](ARCHITECTURE.md) - Deep dive into agent design
- [API Integration](API_INTEGRATION.md) - Detailed API setup
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues & solutions

## 🆘 Need Help?

- Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- Open an [Issue](https://github.com/AmmarAhm3d/autoleadgen/issues)
- Start a [Discussion](https://github.com/AmmarAhm3d/autoleadgen/discussions)

---

**Ready to generate leads? Run your first campaign now! 🚀**
