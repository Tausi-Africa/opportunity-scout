# BSA Opportunity Scout

Automated weekly system that uses Claude AI to research Tanzania consulting opportunities across 50+ sources, compile a verified CSV report, upload it to Google Drive, and deliver a formatted HTML email to the team every Monday morning.

---

## How it works

```
┌────────────────────────────────────────────────────────────────┐
│  Claude.ai Routine — every Monday 09:00 AM EAT                    │
│                                                                 │
│  1. Read SKILL.md from connected GitHub repo                   │
│  2. Read company knowledge files + additional_urls.txt         │
│  3. Plan + execute search across all 13 source categories      │
│     └── 50+ portals: UN agencies, DFIs, embassies, aggregators│
│  4. Filter, verify URLs, score relevance (High/Medium/Low)     │
│  5. Compile CSV (14 columns, strict no-fabrication rules)      │
│  6. Upload CSV to Google Drive → OpportunityScout Reports/     │
│  7. Send HTML email via Gmail connector with CSV attached       │
│     └── To: alex@bsa.ai / CC: rwebu, mnzava                   │
└────────────────────────────────────────────────────────────────┘
```

---

## Project structure

```
opportunity-scout/
├── .claude/
│   └── skills/
│       └── opportunity-scout/
│           └── SKILL.md              # Full operating instructions for the routine
├── knowledgebase/
│   ├── company_profile.txt            # AfroPavo company profile
│   └── additional_urls.txt            # Priority portals to search first
├── instruction.md                     # Step-by-step routine instructions (copy into Claude.ai)
└── README.md
```

---

## Output format

Each run produces a CSV named `OpportunityScout_YYYYMMDD.csv` with 14 columns:

| Column | Description |
|---|---|
| `Opportunity_Title` | Full name exactly as posted |
| `Type` | EOI / RFP / CFP / Tender / Grant / Other |
| `Organization` | Issuing agency — exactly as named |
| `URL` | Verified, working direct link |
| `Contact_Email` | As found — `Not Found` if absent |
| `Contact_Phone` | As found — `Not Found` if absent |
| `Contact_Person` | As named — `Not Found` if absent |
| `Deadline` | YYYY-MM-DD — `Not Stated` if absent |
| `Qualification_Criteria` | Stated criteria only — `Not Found` if none |
| `Consortium_Allowed` | Yes / No / Not Stated |
| `Description` | 2–3 sentence summary from source |
| `Relevance_Score` | High / Medium / Low |
| `Flags` | Eligibility concerns — `None` if clean |
| `Date_Found` | Run date in YYYY-MM-DD |

**Accuracy rule:** every field contains real extracted data, `Not Found`, or `Not Stated`. Nothing is ever guessed or approximated. Opportunities without a verified working URL are excluded entirely.

---

## Sources searched

The routine searches 13 source categories on every run:

| # | Category | Examples |
|---|---|---|
| 1 | Priority URLs | Every URL in `additional_urls.txt` — searched first |
| 2 | LinkedIn | EOI/RFP/tender searches for Tanzania + East Africa |
| 3 | Tanzania Government | PPRA, eGP Portal, Ministry of Finance, ICT, TRA |
| 4 | Development Finance | World Bank, AfDB, IFC, UNCDF, EIB |
| 5 | UN & Multilateral | UNDP, UNICEF, UN Women, FAO, WFP, ILO, WHO |
| 6 | Bilateral Donors | USAID, GIZ, FCDO, EU, SIDA, Norad, DANIDA, MCC, Gates |
| 7 | Financial / Fintech | FSDT, FSD Africa, CGAP, GSMA, Accion, Cenfri, BFA Global |
| 8 | Agriculture & Climate | AGRA, IFAD, CGIAR, GIZ AgriFinance, USAID Feed the Future |
| 9 | Tender Aggregators | Devex, DevelopmentAid, TenderTanzania, dgMarket, ReliefWeb, ImpactPool, TED, SAM.gov |
| 10 | Global Opportunity Platforms | opportunitiesforyouth.org, opportunitydesk.org, Idealist, GlobalGiving, Open Society, Ford, Rockefeller, Mastercard, Aga Khan |
| 11 | Embassies in Tanzania | 25 missions — US, UK, Germany, France, Japan, India, Canada, Australia, Netherlands, Sweden, Norway, Denmark, Finland, Switzerland, Belgium, Italy, South Africa, EU Delegation, China, Turkey, South Korea, Ireland, Brazil, Russia, Spain |
| 12 | Consulting & Innovation Hubs | Tony Elumelu Foundation, Catalyst Fund, Hivos, Ifakara Innovation Hub, BID Network |
| 13 | Research & Academic | J-PAL Africa, IPA, IGC Tanzania, ODI, CGDEV, 3ie |

---

## Email delivery

Every run sends a formatted HTML email:

- **Subject:** `OpportunityScout Weekly Report — YYYY-MM-DD`
- **To:** alex@bsa.ai
- **CC:** rwebu@bsa.ai, mnzava@gmail.com, mnzava@afropavoanalytics.com
- **Body:** Stats banner (Total / High / Medium / Low), top opportunity callout, Google Drive link, attachment note — fully HTML-formatted and character-escaped
- **Attachment:** `OpportunityScout_YYYYMMDD.csv` attached directly
- **Google Drive:** CSV also uploaded to `OpportunityScout Reports/` with public view link

If Google Drive is unavailable, the email is sent with attachment only. If Gmail also fails, the full CSV is displayed in the routine response for manual sending.

---

## Setup

### 1. Connect the GitHub repository

In your Claude.ai project settings, connect this repository so the routine can read files from it.

### 2. Connect Gmail and Google Drive

In your Claude.ai project, enable the **Gmail** and **Google Drive** integrations.

### 3. Add the routine

1. Go to your Claude.ai project → **Routines**
2. Create a new routine scheduled for every Monday at your preferred time
3. Copy the full contents of [instruction.md](instruction.md) and paste it into the routine instruction box

The routine follows 9 steps automatically, with a verification checkpoint after each one.

---

## Updating the company profile

Edit [knowledgebase/company_profile.txt](knowledgebase/company_profile.txt) directly in the repository. The routine reads it fresh on every run — no other changes needed. For richer context, also update the project knowledge files (`afropavo_company_data_a.md`, `afropavo_company_data_b.md`) in the Claude.ai project.

---

## Adding priority search URLs

Add one URL per line to [knowledgebase/additional_urls.txt](knowledgebase/additional_urls.txt). The routine treats every URL in this file as a Priority 1 source and searches it before all other categories.
