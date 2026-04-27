---
name: opportunity-scout
description: Runs a full Tanzania consulting opportunity scan for AfroPavo Analytics Limited, searching 10+ source categories, scoring relevance, compiling results into a CSV, uploading to Google Drive, and sending a formatted HTML email with the CSV attached.
---

# OpportunityScout — AfroPavo Analytics

## What this skill does

Runs a full Tanzania consulting opportunity scan on behalf of AfroPavo Analytics Limited.
Each run: reads company files → searches 10+ source categories with targeted keyword combinations → extracts verified opportunities → scores relevance → compiles a CSV → **uploads the CSV to Google Drive** → **sends a formatted HTML email via Gmail** (with the CSV attached directly and a Google Drive link in the body) to alex@bsa.ai, rwebu@bsa.ai, mnzava@gmail.com, and mnzava@afropavoanalytics.com.

---

## STARTUP — DO THIS FIRST, EVERY RUN

Before any searching, read all three project knowledge files:

1. **`afropavo_company_data_a.md`** — company overview, services, industries, team, case studies
2. **`afropavo_company_data_b.md`** — additional projects, team bios, references
3. **`additional_urls.txt`** — extra URLs to add to the search queue (treat as Priority 1)

Do not begin searching until all three files are read. At the top of every response confirm:

```
✅ afropavo_company_data_a.md — read successfully
✅ afropavo_company_data_b.md — read successfully
✅ additional_urls.txt — read successfully, [N] additional URLs loaded
```

If any file is missing, flag it clearly and continue with what is available.

---

## STRICT ACCURACY RULE — ABSOLUTE, NON-NEGOTIABLE

**Never fabricate, guess, infer, or approximate any field.**

| Situation | What to write |
|---|---|
| Deadline not explicitly stated | `Not Stated` |
| Contact email not found | `Not Found` |
| Contact phone not found | `Not Found` |
| Contact person not named | `Not Found` |
| Qualification criteria not specified | `Not Found` |
| URL cannot be verified as real and working | **Exclude the opportunity entirely** |
| Not certain the opportunity exists | **Exclude the opportunity entirely** |

A report with 3 verified opportunities is better than one with 10 invented ones. Empty and "Not Found" fields are always correct. Filled-in guesses are never acceptable.

---

## COMPANY PROFILE — AFROPAVO ANALYTICS LIMITED

> Always defer to the uploaded company files for the most accurate and complete picture.

**Core Services**
- Data Analytics & AI / Machine Learning
- Credit Risk Modeling & Financial Inclusion
- Digital Transformation & Software Development
- Market Research & Business Analysis
- Strategy Advisory & Innovation
- Blockchain (supply chain, smart contracts, digital assets)
- Risk Management & Insurance
- Organizational & Operations Strategy
- Renewable Energy Strategy & Feasibility Studies
- Investment Advisory & Due Diligence

**Primary Industries**
- Financial Services & Fintech (strongest track record)
- Agriculture & Agri-finance
- Telecommunications & Technology
- Insurance & Microinsurance
- Informal Economy & Savings Groups
- Energy & Climate

**Geography**
- Headquartered in Dar es Salaam, Tanzania
- Active across East Africa (Kenya, Uganda, Rwanda)
- Pan-African research experience across 10+ countries

**Key Clients & Partners**
FSDT, Vodacom, FINCA, Azania Bank, Selcom, Absa, CRDB, ZSSF, Britam, Ifakara Innovation Hub, UNICEF Tanzania, Credit Info, Wakandi

**Subsidiary — Black Swan (bsa.ai)**
AI-powered credit scoring for Africa's informal economy.

**Notable Past Work**
- AI credit scoring reducing loan defaults by 30% (Tausi/Selcom)
- MANKA — open financing AI credit tool adopted by Credit Info
- Gold supply chain blockchain with NFT provenance verification
- Biometric onboarding system for FINCA Microfinance Bank
- Financial inclusion mapping across 10 African countries (FSDT)
- Tanzania Vision 2050 financial sector strategy
- Wakandi CAMS localization for MFIs and SACCOs
- Micro-health insurance design for Britam Tanzania

**Team Strengths**
- Fintech & credit scoring — Derick Kazimoto (Masters FinTech, UCT)
- AI/ML & data science — Anthony Mipawa
- Software engineering — Harvey Kadyanji
- Business analysis & financial research — Alex Mkwizu
- Strategy & enterprise — Rwebugisa Mutahaba (LSE, Cardiff)
- Academic AI & research — Dr. Said Baadel (PhD CS, ex-Deloitte)

---

## WHERE TO SEARCH

### Priority 1 — URLs from `additional_urls.txt`
Read the file and search every URL listed before moving to any default source below.

### 2. LinkedIn
- `EOI Tanzania consulting`
- `RFP Tanzania data analytics`
- `tender Tanzania fintech`
- `call for proposals Tanzania digital`
- `expression of interest Tanzania AI`
- `consulting opportunity Tanzania financial inclusion`
- `RFP East Africa technology consulting`
- `tender East Africa data`

### 3. Tanzania Government Portals
- PPRA — **ppra.go.tz**
- Tanzania eGP Portal — **egp.go.tz**
- Ministry of Finance, Agriculture, ICT Tanzania
- TANESCO, NIDA, TRA, BRELA procurement pages

### 4. Development Finance Institutions
- World Bank — **projects.worldbank.org** (filter: Tanzania)
- African Development Bank — **afdb.org/en/projects-and-operations**
- IFC — **ifc.org**
- UNCDF — **uncdf.org**
- European Investment Bank — **eib.org**

### 5. UN & Multilateral Agencies
- UNDP Tanzania — **undp.org/tanzania** + **procurement.undp.org**
- UNICEF Tanzania — **unicef.org/tanzania**
- UN Women, FAO, WFP, ILO, WHO Tanzania procurement pages

### 6. Bilateral Donors & Implementers
- USAID Tanzania — **usaid.gov** + **sam.gov**
- GIZ Tanzania — **giz.de**
- FCDO / UK Aid — **find-tender.service.gov.uk**
- EU Delegations — **intpa.ec.europa.eu**
- SIDA, Norad, DANIDA Tanzania programs
- MCC — **mcc.gov**
- Bill & Melinda Gates Foundation grants

### 7. Financial Sector & Fintech-Specific
- FSDT Tanzania — **fsdt.or.tz** *(key partner — check every run)*
- FSD Africa — **fsdafrica.org**
- CGAP — **cgap.org**
- GSMA — **gsma.com**
- Accion — **accion.org**
- Cenfri — **cenfri.org**
- BFA Global — **bfaglobal.com**
- FinMark Trust — **finmark.org.za**

### 8. Agriculture & Climate
- AGRA — **agra.org**
- IFAD — **ifad.org**
- CGIAR — **cgiar.org**
- GIZ AgriFinance programs
- USAID Feed the Future Tanzania

### 9. Tender Aggregator Platforms
- Devex — **devex.com/jobs** (filter: Tanzania, consulting)
- DevelopmentAid — **developmentaid.org**
- TenderTanzania — **tendertanzania.co.tz**
- Tender254 — **tender254.com**
- Africa Tenders — **africa-tenders.com**
- dgMarket — **dgmarket.com**
- ReliefWeb — **reliefweb.int** (filter: Tanzania, RFP/EOI)
- ImpactPool — **impactpool.org** (filter: Tanzania, consulting)
- EU Tenders (TED) — **ted.europa.eu** (filter: Tanzania, services)
- Contracts Finder UK — **find-tender.service.gov.uk**
- SAM.gov — **sam.gov** (filter: Tanzania, international)
- East Africa Tenders — **eastafricatenders.com**
- Global Tenders — **globaltenders.eu** (filter: Tanzania)
- Public Tendering — **publictendering.com** (filter: Tanzania)
- UN Tenders — **ungm.org** *(already in priority list — check again here)*

### 10. Global Opportunity & Youth/Development Platforms
- Opportunities for Youth — **opportunitiesforyouth.org**
- Opportunity Desk — **opportunitydesk.org**
- Opportunities Circle — **opportunitiescircle.com**
- Scholars4Dev — **scholars4dev.com**
- AfricanGrantsDatabase — **africangrantsdatabase.com**
- Idealist — **idealist.org** (filter: Tanzania, consulting)
- Bond UK — **bond.org.uk/jobs**
- K4D (Knowledge for Development) — **k4d.info**
- Eldis — **eldis.org**
- Global Giving — **globalgiving.org** (filter: Tanzania)
- Open Society Foundations — **opensocietyfoundations.org/grants**
- Ford Foundation — **fordfoundation.org/work/our-grants**
- Rockefeller Foundation — **rockefellerfoundation.org/grants**
- Wellcome Trust — **wellcome.org/grant-funding**
- Mastercard Foundation — **mastercardfdn.org/opportunities**
- Aga Khan Development Network — **akdn.org/where-we-work/east-africa/tanzania**

### 11. Embassies & High Commissions in Tanzania
Search each embassy's official website for procurement notices, consulting calls, and grant opportunities. Filter for pages titled "tenders", "procurement", "grants", "contracts", or "business opportunities".

| Embassy / High Commission | Website |
|---|---|
| United States Embassy Tanzania | **tz.usembassy.gov/contract-opportunities** |
| British High Commission Tanzania | **gov.uk/world/organisations/british-high-commission-dar-es-salaam** |
| German Embassy Tanzania | **tansania.diplo.de** |
| French Embassy Tanzania | **tz.ambafrance.org** |
| Japanese Embassy Tanzania | **tz.emb-japan.go.jp** |
| Indian High Commission Tanzania | **hcindiatz.gov.in/tenders-tanzania.php** |
| Canadian High Commission Tanzania | **canadainternational.gc.ca/tanzania-tanzanie** |
| Australian High Commission Tanzania | **tanzania.highcommission.gov.au** |
| Netherlands Embassy Tanzania | **tanzania.nlembassy.org** |
| Swedish Embassy Tanzania | **swedenabroad.se/en/embassies/tanzania-dar-es-salaam** |
| Norwegian Embassy Tanzania | **norway.or.tz** |
| Danish Embassy Tanzania | **tanzania.um.dk** |
| Finnish Embassy Tanzania | **finland.or.tz** |
| Swiss Embassy Tanzania | **eda.admin.ch/dares-salaam** |
| Belgian Embassy Tanzania | **diplomatie.belgium.be/tanzania** |
| Italian Embassy Tanzania | **ambdarsalaam.esteri.it** |
| South African High Commission Tanzania | **dirco.gov.za/dar-es-salaam** |
| EU Delegation Tanzania | **eeas.europa.eu/delegations/tanzania** |
| Chinese Embassy Tanzania | **tz.china-embassy.gov.cn** |
| Turkish Embassy Tanzania | **dares.emb.mfa.gov.tr** |
| South Korean Embassy Tanzania | **overseas.mofa.go.kr/tz-en** |
| Irish Embassy Tanzania | **ireland.ie/en/tanzania** |
| Brazilian Embassy Tanzania | **dares-salaam.itamaraty.gov.br** |
| Russian Embassy Tanzania | **tanzania.mid.ru** |
| Spanish Embassy Tanzania | **exteriores.gob.es/tanzania** |

### 12. Consulting & Innovation Hubs
- Tony Elumelu Foundation — **tefconnect.com**
- Catalyst Fund — **catalyst.fund**
- Hivos East Africa — **hivos.org**
- Ifakara Innovation Hub *(known partner — check directly)*
- BID Network — **bidnetwork.org**
- Africa Recruit — **jobs.africarecruit.com**

### 13. Research & Academic Opportunities
- J-PAL Africa — **povertyactionlab.org**
- IPA — **poverty-action.org**
- IGC Tanzania — **theigc.org**
- ODI — **odi.org**
- CGDEV — **cgdev.org**
- 3ie (International Initiative for Impact Evaluation) — **3ieimpact.org**

---

## KEYWORD COMBINATIONS

Use across all sources combined with "Tanzania" or "East Africa":

**Service-based:**
`data analytics consulting`, `AI consulting`, `machine learning RFP`, `digital transformation tender`, `fintech consulting`, `credit scoring`, `financial inclusion consulting`, `market research RFP`, `business analysis EOI`, `software development tender`, `blockchain consulting`, `risk management RFP`, `investment advisory EOI`, `data science consultancy`

**Sector-based:**
`agriculture digitization`, `agri-finance`, `microfinance technology`, `SACCO management`, `insurance technology`, `insurtech`, `mobile money`, `digital payments`, `renewable energy feasibility`, `climate finance`, `informal economy`, `digital lending`

**Output-based:**
`expression of interest`, `EOI`, `request for proposals`, `RFP`, `call for proposals`, `CFP`, `tender notice`, `consultancy`, `individual consultant`, `firm consultant`, `short-term consultancy`

---

## INFORMATION EXTRACTION

For every opportunity, extract these fields exactly. Write `Not Found` or `Not Stated` — never leave blank, never guess.

| Field | Instructions |
|---|---|
| `Opportunity_Title` | Full name exactly as posted |
| `Type` | EOI / RFP / CFP / Tender / Grant / Other — only what is stated |
| `Organization` | Client or posting agency — exactly as named |
| `URL` | Direct link — must be verified and working. Exclude if unverifiable |
| `Contact_Email` | Exactly as found — `Not Found` if absent |
| `Contact_Phone` | Exactly as found — `Not Found` if absent |
| `Contact_Person` | Exactly as named — `Not Found` if absent |
| `Deadline` | YYYY-MM-DD if explicitly stated — otherwise `Not Stated` |
| `Qualification_Criteria` | Only criteria explicitly stated — `Not Found` if none |
| `Consortium_Allowed` | Yes / No / Not Stated — only what is explicitly mentioned |
| `Description` | 2–3 sentence summary based strictly on source content |
| `Relevance_Score` | High / Medium / Low (see scoring guide below) |
| `Flags` | Eligibility concerns based on stated criteria — `None` if no concerns |
| `Date_Found` | Today's actual date in YYYY-MM-DD format |

**PDF & Document Handling:** Open and read the full document. Extract only what is explicitly written. If a field is not in the document, write `Not Found`.

---

## RELEVANCE SCORING

**HIGH** — Direct match to AfroPavo's core work:
- Financial inclusion, fintech, credit, digital finance
- Data analytics, AI/ML, digital transformation
- Market research in AfroPavo's sectors
- Agriculture + technology or data
- Insurance/microinsurance design or technology
- Organizations AfroPavo has worked with before

**MEDIUM** — Partial or adjacent match:
- General ICT or software development
- Research or M&E in relevant sectors
- Strategy advisory in familiar sectors
- Energy feasibility or climate data
- Blockchain or supply chain in any sector

**LOW** — Weak match — include only if the organization or scale is notable

**EXCLUDE entirely:**
- Construction, infrastructure, physical goods procurement
- Legal, audit, accounting, medical/clinical services
- Opportunities requiring government entity status
- Any opportunity without a verified, working URL

---

## RESPONSE STRUCTURE

Every response must contain these sections in order:

### `<file_confirmation>`
Confirm each file was read or flag missing/unreadable files.

### `<search_summary>`
Sources searched, queries used, URLs loaded from `additional_urls.txt`, inaccessible sources and what was done instead.

### `<opportunities_found>`
Total verified opportunities broken down by relevance score. State explicitly if none were found at a source.

### `<key_findings>`
The 3–5 most promising verified opportunities — explain specifically why each fits AfroPavo.

### `<csv_data>`
Complete CSV with columns in this exact order:
```
Opportunity_Title,Type,Organization,URL,Contact_Email,Contact_Phone,Contact_Person,Deadline,Qualification_Criteria,Consortium_Allowed,Description,Relevance_Score,Flags,Date_Found
```
All fields must contain real extracted data or `Not Found` / `Not Stated`. No field may be blank or invented.

### `<recommended_next_steps>`
Opportunities to act on first, confirmed deadlines within 30 days, anything requiring immediate attention.

### `<google_drive_instructions>`
Whether the Google Drive upload succeeded, the folder used, the shareable link, and the file ID. If failed, state the reason clearly.

### `<email_instructions>`
Whether the Gmail send succeeded or failed, and whether the CSV was attached. If failed, state the reason clearly and display the full CSV here for manual sending.

---

## STEP 1 — GOOGLE DRIVE UPLOAD

After the CSV is compiled, upload it using the **Google Drive connector** before sending any email.

**Filename:** `OpportunityScout_[YYYY-MM-DD].csv`
**Target folder:** `OpportunityScout Reports` (create it if it does not exist)
**Permissions:** Set sharing to "Anyone with the link can view" so all email recipients can open it directly.

After a successful upload:
- Record the **shareable link** (e.g. `https://drive.google.com/file/d/FILE_ID/view`)
- Record the **file ID** for reference

If the upload fails:
- Log the error clearly under `<google_drive_instructions>`
- Continue to Step 2 (send the email with only the CSV attachment — no Drive link)

---

## STEP 2 — EMAIL DELIVERY (GMAIL CONNECTOR)

After the Google Drive upload, send the email via the **Gmail connector**.

**To:** alex@bsa.ai
**CC:** rwebu@bsa.ai, mnzava@gmail.com, mnzava@afropavoanalytics.com
**Subject:** `OpportunityScout Weekly Report — [YYYY-MM-DD]`
**Attachment:** attach the CSV file directly as `OpportunityScout_[YYYY-MM-DD].csv`

**Body — use the HTML template below, substituting all `[placeholders]` with real values.
All dynamic text must be HTML-escaped (replace `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`).
The Subject line must be a single line with no newlines or markdown.**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;color:#222;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:24px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);">

        <!-- Header -->
        <tr>
          <td style="background:#1a3a5c;padding:28px 32px;">
            <p style="margin:0;font-size:11px;color:#8ab4d8;letter-spacing:1px;text-transform:uppercase;">AfroPavo Analytics</p>
            <h1 style="margin:6px 0 0;font-size:22px;color:#ffffff;font-weight:700;">OpportunityScout Weekly Report</h1>
            <p style="margin:4px 0 0;font-size:13px;color:#a8c8e8;">[YYYY-MM-DD]</p>
          </td>
        </tr>

        <!-- Stats Banner -->
        <tr>
          <td style="background:#e8f0fe;padding:16px 32px;border-bottom:1px solid #d0ddf5;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="font-size:13px;color:#1a3a5c;padding:4px 16px 4px 0;border-right:1px solid #c0cfe8;text-align:center;">
                  <strong style="font-size:22px;display:block;">[TOTAL]</strong>Total Found
                </td>
                <td style="font-size:13px;color:#2e7d32;padding:4px 16px;border-right:1px solid #c0cfe8;text-align:center;">
                  <strong style="font-size:22px;display:block;">[HIGH]</strong>High Relevance
                </td>
                <td style="font-size:13px;color:#e65100;padding:4px 16px;border-right:1px solid #c0cfe8;text-align:center;">
                  <strong style="font-size:22px;display:block;">[MEDIUM]</strong>Medium Relevance
                </td>
                <td style="font-size:13px;color:#555;padding:4px 16px;text-align:center;">
                  <strong style="font-size:22px;display:block;">[LOW]</strong>Low Relevance
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Top Opportunity -->
        <tr>
          <td style="padding:24px 32px 12px;">
            <h2 style="margin:0 0 10px;font-size:14px;font-weight:700;color:#1a3a5c;
                        text-transform:uppercase;letter-spacing:.5px;
                        border-bottom:2px solid #1a3a5c;padding-bottom:6px;">
              Top Opportunity This Week
            </h2>
            <p style="margin:0;font-size:14px;line-height:1.7;color:#333;">
              [One sentence describing the single most promising verified opportunity and why it fits AfroPavo]
            </p>
          </td>
        </tr>

        <!-- Google Drive Link -->
        <tr>
          <td style="padding:8px 32px 12px;">
            <h2 style="margin:0 0 10px;font-size:14px;font-weight:700;color:#1a3a5c;
                        text-transform:uppercase;letter-spacing:.5px;
                        border-bottom:2px solid #e0e0e0;padding-bottom:6px;">
              View &amp; Download Report
            </h2>
            <p style="margin:0;padding:14px 18px;background:#e8f0fe;border-left:4px solid #1a3a5c;
                       border-radius:4px;font-size:13px;color:#1a3a5c;">
              &#128193; This report has been saved to Google Drive:<br><br>
              <a href="[GOOGLE_DRIVE_LINK]"
                 style="color:#1a3a5c;font-weight:700;word-break:break-all;">[GOOGLE_DRIVE_LINK]</a>
            </p>
          </td>
        </tr>

        <!-- Attachment Note -->
        <tr>
          <td style="padding:8px 32px 24px;">
            <p style="margin:0;padding:14px 18px;background:#f0f7ee;border-left:4px solid #2e7d32;
                       border-radius:4px;font-size:13px;color:#2e7d32;">
              &#128206; The CSV is also attached directly to this email:
              <strong>OpportunityScout_[YYYY-MM-DD].csv</strong>
            </p>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f8f9fa;padding:16px 32px;border-top:1px solid #e0e0e0;">
            <p style="margin:0;font-size:12px;color:#888;text-align:center;">
              OpportunityScout &nbsp;|&nbsp; AfroPavo Analytics &nbsp;|&nbsp;
              <a href="https://www.afropavoanalytics.com"
                 style="color:#1a3a5c;text-decoration:none;">afropavoanalytics.com</a>
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
```

**If Google Drive upload failed:** replace the "View & Download Report" section with:
```html
<tr>
  <td style="padding:8px 32px 12px;">
    <p style="margin:0;padding:14px 18px;background:#fff3e0;border-left:4px solid #e65100;
               border-radius:4px;font-size:13px;color:#e65100;">
      &#9888; Google Drive upload was not available this run.
      The full CSV is attached directly to this email.
    </p>
  </td>
</tr>
```

If both Google Drive and Gmail fail, display the full CSV in the response under `<email_instructions>` so it can be sent manually.

---

## STANDING RULES

- **Never make up data. If it is not found, write `Not Found` or `Not Stated`. This is absolute.**
- Read all three project files at the start of every run — no exceptions
- Search all source categories every run — postings change weekly
- If a source is inaccessible, note it and try an alternative
- Prioritize opportunities with confirmed deadlines within the next 30 days
- Do not include any opportunity without a verified, working URL
- **Always attempt Google Drive upload before sending the email**
- The email Subject must be a single plain-text line — no markdown, no newlines
- All dynamic content in the email body must be HTML-escaped before insertion
- If Google Drive is unavailable, send the email with CSV attachment only (no Drive link)
- If Gmail is also unavailable, display the full CSV in the response under `<email_instructions>`
- Accuracy is the highest priority — a short accurate report beats a long fabricated one

---

## DELIVERY RECIPIENTS

| Role | Address |
|---|---|
| To | alex@bsa.ai |
| CC | rwebu@bsa.ai |
| CC | mnzava@gmail.com |
| CC | mnzava@afropavoanalytics.com |

Google Drive folder: **OpportunityScout Reports** (create if absent, set link-sharing to "Anyone with link can view")
