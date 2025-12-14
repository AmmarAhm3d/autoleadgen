# Contributing Guide

Thank you for interest in contributing to AutoLeadGen! This guide will help you get started.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct:

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive criticism
- Report issues privately if needed

## 📋 Getting Started

### 1. Fork & Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/AmmarAhm3d/autoleadgen.git
cd autoleadgen

# Add upstream remote
git remote add upstream https://github.com/original/autoleadgen.git
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name

# Branch naming conventions:
# - feature/add-new-agent
# - bugfix/fix-email-extraction
# - docs/update-readme
# - refactor/improve-performance
```

### 3. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## 🔧 Development Workflow

### Writing Code

#### Code Style
- Follow PEP 8 conventions
- Use type hints
- Max line length: 100 characters
- Use descriptive variable names

```python
# ✅ Good
def extract_email_from_website(
    url: str,
    timeout: int = 30
) -> Optional[str]:
    """Extract email from website using Firecrawl."""
    pass

# ❌ Poor
def extract(u, t=30):
    pass
```

#### File Organization
```
src/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Abstract base class
│   ├── scraper_agent.py   # Scraper implementation
│   └── enrichment_agent.py
├── tools/
│   ├── __init__.py
│   ├── yelp_scraper.py
│   └── firecrawl_client.py
└── models/
    ├── __init__.py
    └── lead.py
```

### Testing

#### Write Tests
Every feature should include tests:

```python
# tests/test_enrichment_agent.py
import pytest
from autoleadgen.agents import EnrichmentAgent

@pytest.fixture
def enricher():
    return EnrichmentAgent()

def test_extract_email_success(enricher):
    """Test successful email extraction."""
    result = enricher.extract_email("https://example.com")
    assert result is not None
    assert "@" in result

def test_extract_email_timeout(enricher):
    """Test timeout handling."""
    with pytest.raises(TimeoutError):
        enricher.extract_email("https://slow-site.com", timeout=1)
```

#### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_agents.py -v

# Run single test
pytest tests/test_agents.py::test_extract_email_success -v
```

#### Coverage Requirements
- Minimum 80% code coverage for new code
- Run: `pytest --cov=src --cov-report=term-missing`

### Documentation

#### Docstrings
Use Google-style docstrings:

```python
def enrich_lead(
    lead: dict,
    include_owner: bool = True
) -> dict:
    """Enrich lead with contact information.
    
    Args:
        lead: Lead dictionary with minimal info
        include_owner: Whether to extract owner info
        
    Returns:
        Lead dictionary with additional contact fields
        
    Raises:
        TimeoutError: If enrichment takes too long
        APIError: If API calls fail
        
    Example:
        >>> lead = {"company_name": "ABC Corp"}
        >>> enriched = enrich_lead(lead)
        >>> "email" in enriched
        True
    """
    pass
```

#### README for New Modules
Add a README.md to complex modules:

```markdown
# Email Extraction Tool

## Overview
Extracts email addresses from business websites using Firecrawl.

## Usage
```python
from src.tools import extract_email
email = extract_email("https://example.com")
```

## Configuration
- `timeout`: Request timeout in seconds (default: 30)
- `verify`: Verify email validity (default: True)
```

## 🔄 Commit Workflow

### Before Committing

```bash
# Format code
black src/ tests/

# Check style
flake8 src/

# Type checking
mypy src/

# Run tests
pytest
```

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>

# Types: feat, fix, docs, refactor, test, chore, perf
# Example:
feat(enrichment): add email verification via mailmodo API

- Implement email verification with mailmodo
- Add retry logic for failed verifications
- Update configuration options

Closes #42
```

### Commit Examples

```bash
git commit -m "feat(scraper): add government directory support"

git commit -m "fix(enrichment): handle timeout in firecrawl calls"

git commit -m "docs(api): add API integration guide"

git commit -m "refactor(agents): improve error handling in base agent"

git commit -m "test(qualification): add tests for lead scoring"
```

## 🔀 Pull Request Process

### 1. Sync with Upstream

```bash
# Fetch latest changes
git fetch upstream

# Rebase on main
git rebase upstream/main
```

### 2. Push Branch

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

**PR Title Format:**
```
feat(component): Brief description of changes
```

**PR Description Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Added tests for new functionality
- [ ] All tests pass locally
- [ ] Tested in development environment

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Added changelog entry
```

### 4. PR Review

- Address reviewer feedback promptly
- Request re-review after making changes
- Keep discussions respectful and constructive

## 🎯 Areas for Contribution

### High Priority
- [ ] Add more data sources (LinkedIn, Indeed, etc.)
- [ ] Improve email extraction accuracy
- [ ] Add CRM integrations (Salesforce, HubSpot)
- [ ] Performance optimizations

### Medium Priority
- [ ] Improve logging and monitoring
- [ ] Add more data validation
- [ ] Expand test coverage
- [ ] Create example notebooks

### Good for Beginners
- [ ] Fix typos in documentation
- [ ] Improve error messages
- [ ] Add code comments
- [ ] Create usage examples
- [ ] Update README examples

## 🐛 Bug Reports

### Creating a Bug Report

1. **Check existing issues** - Avoid duplicates
2. **Create detailed report**:
   ```
   Title: [Bug] Brief description
   
   Environment:
   - OS: Ubuntu 20.04
   - Python: 3.11
   - AutoLeadGen: v0.1.0
   
   Steps to reproduce:
   1. Do X
   2. Do Y
   3. See error
   
   Expected behavior:
   Should do Z
   
   Actual behavior:
   Gets error: ...
   
   Logs:
   [error logs here]
   ```

## 🎨 Feature Requests

### Creating a Feature Request

```
Title: [Feature] Brief description

Problem:
Describe the problem you're trying to solve

Solution:
Describe your proposed solution

Alternatives:
Describe alternative approaches

Additional context:
Add any other context
```

## 📚 Documentation Contributions

### Improve Existing Docs

```bash
# Edit documentation
vim docs/ARCHITECTURE.md

# Build documentation (if using Sphinx)
cd docs && make html

# Test links
python -m linkchecker docs/
```

### Add New Documentation

```markdown
# New Feature Documentation

## Overview
Brief explanation of the feature

## Setup
Installation and configuration steps

## Usage
Code examples and common patterns

## Troubleshooting
Common issues and solutions

## References
Links to related documentation
```

## 🚀 Deployment & Release

### Version Numbering
Following semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### Creating a Release

```bash
# Update version in setup.py
# Update CHANGELOG.md
# Create git tag
git tag v0.2.0
git push origin v0.2.0

# GitHub Actions will build and publish
```

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project credit page

## 📞 Getting Help

- **Questions**: Open a Discussion
- **Bug Reports**: Open an Issue with [Bug] label
- **Feature Requests**: Open an Issue with [Feature] label
- **Code Help**: Comment on PR or open Discussion

## 📖 Useful Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)

---

**Thank you for contributing to AutoLeadGen! 🙏**
