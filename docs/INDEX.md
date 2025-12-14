# Documentation Index

Complete documentation for AutoLeadGen.

## 📖 Getting Started

### [Quick Start Guide](QUICK_START.md)
Get up and running in 5 minutes. Covers:
- Installation
- Configuration  
- Running your first campaign
- Viewing results
- Common use cases

**Best for**: New users wanting to start immediately

### [Architecture Guide](ARCHITECTURE.md)
Deep dive into system design. Covers:
- Agent architecture
- Data flow
- CrewAI integration
- LangGraph implementation
- API integration points
- Performance optimization
- Monitoring & logging

**Best for**: Developers wanting to understand the system

### [API Integration Guide](API_INTEGRATION.md)
Complete API setup and usage. Covers:
- Yelp Fusion API setup
- Firecrawl API setup
- Anthropic Claude setup
- OpenAI API setup
- Environment configuration
- Testing connections
- Rate limiting
- Error handling

**Best for**: Setting up API integrations

## 🚀 Deployment & Operations

### [Deployment Guide](DEPLOYMENT.md)
Deploy to various environments. Covers:
- Development setup
- Local production
- Docker deployment
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes deployment
- Monitoring setup
- Maintenance procedures

**Best for**: DevOps engineers and deployment

## 🤝 Contributing

### [Contributing Guide](../CONTRIBUTING.md)
How to contribute to the project. Covers:
- Code of conduct
- Getting started
- Development workflow
- Testing
- Commit conventions
- Pull request process
- Areas for contribution

**Best for**: Contributors and maintainers

## 📋 Project Info

### [README](../README.md)
Project overview and features. Covers:
- Project description
- Tech stack
- Key features
- Quick examples
- Case studies

**Best for**: General project information

### [CHANGELOG](../CHANGELOG.md)
Version history and updates. Covers:
- Release notes
- New features
- Bug fixes
- Deprecations
- Performance improvements
- Roadmap

**Best for**: Tracking project evolution

### [LICENSE](../LICENSE)
MIT License for the project

## 🏗️ Project Structure

```
autoleadgen/
│
├── README.md                    # Project overview
├── CONTRIBUTING.md              # How to contribute
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
│
├── docs/
│   ├── QUICK_START.md          # Get started in 5 minutes
│   ├── ARCHITECTURE.md         # System design & details
│   ├── API_INTEGRATION.md      # API setup guides
│   └── DEPLOYMENT.md           # Deployment instructions
│
├── src/
│   ├── agents/                 # CrewAI agent implementations
│   ├── tools/                  # Reusable tools and utilities
│   ├── models/                 # Data models
│   ├── pipeline.py             # Main orchestration
│   └── utils/                  # Helper functions
│
├── scripts/
│   ├── scrape_example.py       # Example lead scraping
│   ├── enrich_emails.py        # Email enrichment script
│   └── generate_campaigns.py   # Campaign generation
│
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_pipeline.py
│
└── data/
    ├── leads.csv               # Discovered leads
    └── proxies.txt             # Proxy list
```

## 🔍 Quick Navigation by Topic

### I want to...

#### Start using AutoLeadGen
→ [Quick Start Guide](QUICK_START.md)

#### Understand how it works
→ [Architecture Guide](ARCHITECTURE.md)

#### Set up API integrations
→ [API Integration Guide](API_INTEGRATION.md)

#### Deploy to production
→ [Deployment Guide](DEPLOYMENT.md)

#### Contribute to the project
→ [Contributing Guide](../CONTRIBUTING.md)

#### Find what's new
→ [CHANGELOG](../CHANGELOG.md)

#### See example code
→ [Quick Start Guide - Use Cases](QUICK_START.md#-common-use-cases)

#### Troubleshoot an issue
→ [Deployment Guide - Troubleshooting](DEPLOYMENT.md#-troubleshooting)

#### Understand the project structure
→ [Project Structure](#-project-structure) above

## 📊 Documentation Statistics

| Document | Type | Length | Focus |
|----------|------|--------|-------|
| Quick Start | Guide | 5-10 min | Getting started |
| Architecture | Reference | 20-30 min | System design |
| API Integration | Guide | 15-20 min | API setup |
| Deployment | Guide | 20-30 min | Production |
| Contributing | Guide | 10-15 min | Development |
| README | Overview | 10-15 min | Project info |
| CHANGELOG | Reference | 5-10 min | Version history |

## 🔗 External Resources

### CrewAI Documentation
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Docs](https://docs.crewai.com)

### LangGraph Documentation
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

### Firecrawl Documentation
- [Firecrawl Website](https://www.firecrawl.dev)
- [Firecrawl GitHub](https://github.com/mendableai/firecrawl)

### Yelp Fusion API
- [Yelp Developers](https://www.yelp.com/developers)
- [Yelp API Docs](https://docs.developer.yelp.com)

### Anthropic Claude
- [Anthropic Website](https://www.anthropic.com)
- [Claude API Docs](https://docs.anthropic.com)

## 📞 Support

### Getting Help

- **Questions**: Start a [Discussion](https://github.com/AmmarAhm3d/autoleadgen/discussions)
- **Issues**: Report a [Bug](https://github.com/AmmarAhm3d/autoleadgen/issues)
- **Features**: Request a [Feature](https://github.com/AmmarAhm3d/autoleadgen/issues)
- **Discussions**: Join the [Community](https://github.com/AmmarAhm3d/autoleadgen/discussions)

### Documentation Issues

Found a typo or unclear section? Open an issue or submit a PR!

## 🎓 Learning Path

### Beginner
1. Read [README](../README.md)
2. Follow [Quick Start Guide](QUICK_START.md)
3. Run example scripts
4. Try basic API usage

### Intermediate
1. Study [Architecture Guide](ARCHITECTURE.md)
2. Review agent implementations in `src/agents/`
3. Explore [API Integration Guide](API_INTEGRATION.md)
4. Run full pipeline examples

### Advanced
1. Review system architecture
2. Customize agents and tools
3. Deploy to production ([Deployment Guide](DEPLOYMENT.md))
4. Contribute to the project ([Contributing Guide](../CONTRIBUTING.md))

### DevOps
1. Understand [Deployment Guide](DEPLOYMENT.md)
2. Set up monitoring and logging
3. Configure CI/CD pipelines
4. Scale infrastructure

## 📝 Document Conventions

### Code Examples
```python
# Highlighted with language tag
from autoleadgen import LeadGenerationPipeline
```

### Important Notes
> **Note**: This is an important note that should be read

### Warnings
> **⚠️ Warning**: Be careful with this action

### Tips
> **💡 Tip**: A helpful tip or shortcut

## 🔄 Documentation Maintenance

- Documentation is updated with each release
- Last updated: **December 2025**
- Version: **0.2.0**

---

**Happy learning! Start with the [Quick Start Guide](QUICK_START.md) 🚀**
