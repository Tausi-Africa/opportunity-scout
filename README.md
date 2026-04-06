# APA Opportunity Scout

Automated weekly pipeline that scrapes 13+ Tanzania procurement portals, uses Claude AI to assess fit against the company profile, and delivers a colour-coded Excel report to `alex@bsa.ai` every Monday morning.

---

## How it works

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions — every Monday 07:00 EAT                │
│                                                         │
│  1. Run tests (must pass before proceeding)             │
│  2. Claude searches web for new opportunity portals     │
│  3. Scrape 13 known sites + any Claude-discovered sites │
│     ├── Requests + BeautifulSoup for static pages       │
│     └── Playwright + Chromium for JS-rendered pages     │
│  4. Download and parse PDFs found on opportunity pages  │
│  5. Claude assesses each opportunity against            │
│     company profile → fit / nearly_fit / far_fetched    │
│  6. Build colour-coded Excel report                     │
│  7. Email report + summary to alex@bsa.ai               │
└─────────────────────────────────────────────────────────┘
```

---

## Project structure

```
opportunity-scout/
├── scripts/
│   └── main.py                  # Full pipeline (scrape → assess → Excel → email)
├── tests/
│   ├── conftest.py              # Shared pytest fixtures
│   ├── test_scraper.py          # HTTP, HTML parsing, PDF extraction
│   ├── test_assessor.py         # Claude AI fit assessment
│   ├── test_excel_builder.py    # Excel output and colour coding
│   ├── test_email.py            # SMTP sending and fallback
│   └── test_pipeline.py        # End-to-end integration tests
├── knowledgebase/
│   └── company_profile.txt      # Company profile read at runtime
├── .github/
│   └── workflows/
│       └── weekly_scout.yml     # GitHub Actions — tests + scout
├── .env                         # Local credentials (never committed)
└── requirements.txt             # Python dependencies
```

---

## Opportunity sources

| Source | Type | Notes |
|---|---|---|
| UNGM | UN procurement | JS-rendered, Playwright |
| World Bank | Project opportunities | JS-rendered, Playwright |
| EU Tenders | European donor | JS-rendered, Playwright, Tanzania filter |
| US Embassy Tanzania | US government contracts | Static |
| African Development Bank | AfDB procurement | JS-rendered, Playwright |
| GIZ Tanzania | German development | Static |
| GIZ Ausschreibungen | GIZ procurement portal | JS-rendered, Playwright |
| DG Market | Multi-donor tenders | Static, Tanzania filter |
| FSDT | Financial sector deepening | Static |
| CRDB Bank | Bank procurement | Static |
| NBC Bank | Bank procurement | Static |
| NMB Bank | Bank procurement | Static |
| India HC Tanzania | Indian high commission | Static |
| + Claude-discovered | Found fresh each run | Dynamic |

Claude also searches the web at the start of each run to discover new portals (UNDP, PPRA, ministry pages, bilateral donors, etc.) and adds them to the scrape list automatically.

---

## Fit assessment

Each opportunity is assessed by Claude against the company profile and classified as:

| Label | Colour | Meaning |
|---|---|---|
| **fit** | Green | Core services match, eligible, likely meets requirements |
| **nearly_fit** | Yellow | 60–80% match — minor sector or experience gap |
| **far_fetched** | Red | Significant mismatch in sector, geography, or requirements |

For each opportunity, the report captures:

- Title, issuing organisation, opportunity type (RFP / EOI / Call for Tenders)
- Sectors and background context
- Deadline and budget (or notes if budget is to be proposed)
- Eligibility criteria (parsed from page text and PDFs)
- Fit assessment and reasoning
- Contact email and direct application link

---

## Setup

### 1. Fork or clone this repository

```bash
git clone https://github.com/your-org/opportunity-scout.git
cd opportunity-scout
```

### 2. Add GitHub repository secrets

Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your key from [console.anthropic.com](https://console.anthropic.com) |
| `SENDER_EMAIL` | The Gmail/Google Workspace address that sends the report |
| `SENDER_APP_PASSWORD` | 16-character App Password (see below) |

#### Creating a Gmail App Password

1. Sign in to the sender account at [myaccount.google.com](https://myaccount.google.com)
2. Go to **Security → 2-Step Verification** and enable it
3. Go to **Security → App passwords** (or [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords))
4. Name it `BSA Scout` and click **Create**
5. Copy the 16-character password and paste it as `SENDER_APP_PASSWORD`

### 3. Run manually (first test)

Go to your GitHub repo → **Actions** tab → **Weekly BSA Opportunity Scout** → **Run workflow**.

Watch the logs live. On success, `alex@bsa.ai` receives the Excel report within ~20 minutes.

After that, it runs automatically every **Monday at 07:00 EAT** with no further action needed.

---

## Local development

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright's Chromium browser
playwright install chromium

# Copy and fill in credentials
cp .env.example .env           # then edit .env with real values
```

`.env` file format:

```
ANTHROPIC_API_KEY=sk-ant-...
SENDER_EMAIL=alex@bsa.ai
SENDER_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

Run the pipeline locally:

```bash
python scripts/main.py
```

Run the test suite:

```bash
pytest tests/ -v --cov=scripts --cov-report=term-missing
```

---

## Error handling

| Scenario | Behaviour |
|---|---|
| Site returns 404 / 403 | Skipped immediately, no retry |
| Site returns 500 / timeout | Retried up to 3× with exponential backoff |
| Playwright fails on JS site | Falls back to plain requests automatically |
| One site completely unreachable | Logged as error, rest of pipeline continues |
| Claude returns malformed JSON | Assessment skipped, opportunity logged and dropped |
| Claude API rate limit | Logged, assessment skipped for that item |
| SMTP auth fails | Detailed fix instructions logged; email body saved as `.email_body.txt` next to the Excel file |
| No opportunities scraped | Pipeline exits with code 1, warning logged |
| Company profile missing | Pipeline exits with code 2, clear error message |

If email delivery fails for any reason, the full email body is saved alongside the Excel report as a `.email_body.txt` file and uploaded as a GitHub Actions artifact (retained 90 days).

---

## Updating the company profile

Edit [knowledgebase/company_profile.txt](knowledgebase/company_profile.txt) directly. The file is read fresh on every run — no code changes needed. Claude uses it to assess fit, so keep it current with your latest capabilities and sector focus.

---

## Updating target sectors / keywords

Edit the `KEYWORDS` list in [scripts/main.py](scripts/main.py):

```python
KEYWORDS = [
    "research", "data", "analytics", "finance", "credit", "digital",
    "facilitation", "consulting", "advisory", ...
]
```

Only opportunities whose title contains at least one keyword are fetched and assessed. Add domain-specific terms to increase recall.

---

## Adding a new site manually

Add an entry to the `SITES` list in [scripts/main.py](scripts/main.py):

```python
{"name": "Portal Name", "url": "https://portal.org/tenders", "country_filter": None, "use_playwright": False}
```

- Set `country_filter` to `"Tanzania"` if the portal lists global opportunities and needs filtering
- Set `use_playwright` to `True` for portals that require JavaScript to render content

---

## CI/CD pipeline

The GitHub Actions workflow runs two jobs in sequence:

```
test  ──→  scout
```

**`test` job** — runs the full pytest suite with 70% coverage minimum. If any test fails, the scout job does not run.

**`scout` job** — installs Playwright Chromium, runs the pipeline, uploads the Excel report as an artifact regardless of outcome.

Both jobs are triggered by the weekly schedule and by manual dispatch.
