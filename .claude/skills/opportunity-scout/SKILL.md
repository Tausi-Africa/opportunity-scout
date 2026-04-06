---
name: opportunity-scout
description: Scrape Tanzania consulting opportunities (research, data, finance, credit scoring, digital systems, facilitation) from donor and procurement portals. Assess fit against company profile, parse PDFs, extract deadlines and budgets, build Excel report, and email to alex@bsa.ai. Run with /opportunity-scout
context: fork
---

# BSA Opportunity Scout Skill

## Purpose
Find, assess, and report on consulting opportunities in Tanzania across research, data, finance, credit scoring, digital systems, and facilitation services. Deliver a colour-coded Excel report and summary email to alex@bsa.ai.

## Trigger
Run explicitly with `/opportunity-scout` or when asked to "run the weekly scout", "find Tanzania opportunities", or "check procurement portals".

## Step-by-Step Instructions

### Step 1 — Environment Check
Confirm the following exist before proceeding:
- `company_profile.txt` in the project root
- `.env` file containing `SENDER_EMAIL`, `SENDER_APP_PASSWORD`, and `ANTHROPIC_API_KEY`
- Python virtual environment or `pip install -r requirements.txt` has been run

If any are missing, stop and tell the user what is needed.

### Step 2 — Run the Scraper
Execute the main pipeline script:
```bash
python bsa_scout/main.py
```

Monitor output. If a site fails due to JavaScript rendering, note it in the summary. Do not stop the full run for a single site failure.

### Step 3 — Review Output
After the script completes:
- Confirm `output/BSA_Opportunities_YYYYMMDD.xlsx` was created
- Report counts: total found, ✅ Fit, 🟡 Nearly Fit, ❌ Far Fetched
- List top 5 strong-fit opportunities with deadlines

### Step 4 — Email Confirmation
Confirm the email was sent to alex@bsa.ai. If it failed, show the error and offer to retry or save the file locally.

## Target Sectors (for keyword filtering)
- Research & Data Analytics
- Finance & Credit Scoring
- Digital Systems & Technology
- Facilitation & Capacity Building
- Fintech & Financial Inclusion
- Monitoring & Evaluation (M&E)
- Digital Transformation

## Fit Assessment Criteria
Use company_profile.txt as the baseline. Assess each opportunity as:
- **fit** — core services match, location eligible, likely meets experience requirements
- **nearly_fit** — 60–80% match, minor gaps (e.g. slightly outside sector or experience threshold)
- **far_fetched** — significant misalignment in sector, geography exclusion, or unreachable requirements

## Supporting Files
- `bsa_scout/main.py` — full pipeline (scraping → assessment → Excel → email)
- `bsa_scout/scrapers.py` — per-site scraping logic
- `bsa_scout/assessor.py` — Claude API fit assessment
- `bsa_scout/excel_builder.py` — Excel formatting
- `bsa_scout/emailer.py` — SMTP email with attachment
- `company_profile.txt` — read at runtime
- `requirements.txt` — Python dependencies
- `.github/workflows/weekly_scout.yml` — GitHub Actions weekly automation
