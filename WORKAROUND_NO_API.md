# Running Opportunity Scout Without Anthropic API Subscription

If you have **Claude web access** but **no API subscription**, follow this workaround:

## Quick Setup

1. **Don't set `ANTHROPIC_API_KEY` environment variable**
   - Remove it from `.env` or leave it empty
   - The workflow will skip Claude features and continue

2. **The pipeline will:**
   - ✅ Scrape all opportunity websites
   - ✅ Build Excel report with all opportunities
   - ✅ Send email with report
   - ❌ Skip Claude-powered assessment (you manually review instead)

3. **Manual Review Process:**
   - Open the generated Excel file (`output/opportunities_*.xlsx`)
   - Review opportunities manually
   - Assessment categories will be empty (fill in as needed or ignore)

## Why This Works

The code gracefully handles missing API key:

```python
# scripts/main.py (line 51)
if not _api_key:
    log.warning("ANTHROPIC_API_KEY not set — Claude features will fail")

# In assess() function, exceptions are caught and logged
# without stopping the pipeline
```

## GitHub Actions Workflow

The workflow test will **skip the API connectivity test** if no key is set:

```yaml
# .github/workflows/weekly_scout.yml (line 117-130)
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "⚠️  ANTHROPIC_API_KEY not configured"
  exit 0  # Skip test, don't fail workflow
fi
```

## Alternative: Use Free Claude Alternative (Optional)

If you want AI-powered assessment without API subscription:

1. **Ollama + Local Model** (runs on your machine)
   - Install: https://ollama.ai
   - Run: `ollama pull mistral` or `ollama pull neural-chat`
   - Modify scripts/main.py to use local endpoint instead of Anthropic API

2. **Open Router API** (pay-per-use, very cheap)
   - Sign up: https://openrouter.ai
   - Cost: ~$0.01-0.10 per assessment (vs $0.18+ with Anthropic)
   - Update API endpoint in scripts/main.py

## Questions?

- All opportunities will be marked as "fit" (neutral)
- You can manually categorize them after review
- Excel report will still have all scraped data (title, deadline, budget, URLs)

---
**Recommendation:** Run without API key for now. Manually review the Excel output. If you find the assessments valuable, consider:
- Upgrading to Claude API ($5 minimum)
- Using a cheaper alternative (Open Router)
- Setting up local LLM (Ollama)
