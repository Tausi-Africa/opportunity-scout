#!/usr/bin/env python3
"""
BSA Opportunity Scout — main.py
Single Claude call with web search → CSV export → email.
Run: python scripts/main.py
"""

import html
import logging
import os
import re
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).parent.parent
COMPANY_PROFILE = BASE_DIR / "knowledgebase" / "company_profile.txt"
ADDITIONAL_URLS = BASE_DIR / "knowledgebase" / "additional_urls.txt"
OUTPUT_DIR      = BASE_DIR / "output"
RECIPIENT       = "alex@bsa.ai"
SENDER_EMAIL    = os.getenv("SENDER_EMAIL")
SENDER_PASS     = os.getenv("SENDER_APP_PASSWORD")
MODEL           = "claude-sonnet-4-6"

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=300.0,
    max_retries=2,
)

PROMPT_TEMPLATE = """\
You will be acting as a highly experienced research assistant tasked with finding consulting opportunities \
(Expressions of Interest/EOIs and Requests for Proposals/RFPs) relevant to a company's \
profile in Tanzania. Your goal is to search the web, extract relevant information, and \
compile it into a structured CSV format.

Here is the company profile you should use to assess relevance of opportunities:

<company_profile>
{company_profile}
</company_profile>

Here are some starting URLs to search (but you should not limit yourself to only these sources):

<additional_urls>
{additional_urls}
</additional_urls>

The final CSV should be sent to this email address:

<email_address>
{email_address}
</email_address>

Your task involves the following steps:

1. SEARCH STRATEGY:
   - Search for consulting opportunities, EOIs, and RFPs specifically for Tanzania
   - Use the provided URLs as starting points but expand your search to other relevant sources
   - Look for government procurement portals, development agency websites, NGO opportunity \
pages, and consulting tender platforms
   - Focus on opportunities that match the company profile's expertise and capabilities
   - Use a variety of search terms and filters to find the most relevant and up-to-date opportunities
   - Also search for these opportunities in Linkedin posts , twitter and instagram posts, and other social media channels where they may be shared by organizations or individuals in the Tanzanian consulting ecosystem

2. INFORMATION EXTRACTION:
   For each opportunity you find, extract the following information:
   - Opportunity title/name
   - Type (EOI, RFP, tender, etc.)
   - Organization/client posting the opportunity
   - Direct link/URL to the opportunity
   - Contact information (email, phone, contact person if available)
   - Submission deadline
   - Qualification criteria/requirements (if specified)
   - Brief description of the opportunity
   - Relevance score to company profile (High/Medium/Low)

3. DOCUMENT HANDLING:
   - If opportunities are posted as PDFs or other document formats, read and extract the \
relevant information from these documents
   - Pay special attention to eligibility criteria, scope of work, and submission requirements \
within PDFs
   - Extract contact details that may only be available within the document

4. RELEVANCE ASSESSMENT:
   - Compare each opportunity against the company profile
   - Only include opportunities that reasonably match the company's expertise, sector focus, \
and capabilities
   - Note any specific qualification criteria that the company should be aware of

Before compiling your results, use the scratchpad below to plan your search approach:

<scratchpad>
- List the key sectors/expertise from the company profile
- Identify the most relevant search terms and sources
- Plan which websites and portals to prioritize
</scratchpad>

5. OUTPUT FORMAT:
   Compile all opportunities into a CSV file with the following columns:
   - Opportunity_Title
   - Type
   - Organization
   - URL
   - Contact_Email
   - Contact_Phone
   - Contact_Person
   - Deadline
   - Qualification_Criteria
   - Description
   - Relevance_Score
   - Date_Found

   Ensure the CSV is properly formatted with:
   - Headers in the first row
   - Each opportunity in a separate row
   - Commas as delimiters
   - Text fields enclosed in quotes if they contain commas
   - Date format as YYYY-MM-DD for deadlines

6. FINAL DELIVERABLE:
   Your response should include:
   - A summary of your search process and sources consulted
   - The total number of opportunities found
   - A brief analysis of the most promising opportunities
   - The complete CSV data

Present your final output in the following format:

<search_summary>
[Describe your search process, sources used, and any challenges encountered]
</search_summary>

<opportunities_found>
[State the total number of opportunities identified]
</opportunities_found>

<key_findings>
[Highlight 3-5 most relevant/promising opportunities with brief explanations]
</key_findings>

<csv_data>
[Insert the complete CSV data here, properly formatted]
</csv_data>

<email_instructions>
Confirm that this CSV should be sent to {email_address}
</email_instructions>

Note: Your final output should contain the complete CSV data ready to be saved as a file \
and emailed. Ensure all information is accurate and up-to-date, with working URLs and \
valid contact information wherever possible.\
"""


# ── File loaders ──────────────────────────────────────────────────────────────
def load_profile() -> str:
    if not COMPANY_PROFILE.exists():
        raise FileNotFoundError(f"company_profile.txt not found at {COMPANY_PROFILE.resolve()}")
    text = COMPANY_PROFILE.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("company_profile.txt is empty.")
    return text


def load_additional_urls() -> str:
    if not ADDITIONAL_URLS.exists():
        log.warning("additional_urls.txt not found — Claude will search without seed URLs")
        return ""
    return ADDITIONAL_URLS.read_text(encoding="utf-8").strip()


# ── Response helpers ──────────────────────────────────────────────────────────
def extract_section(text: str, tag: str) -> str:
    """Extract content between <tag>…</tag>. Returns '' if not found."""
    match = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def _get_full_text(response: anthropic.types.Message) -> str:
    """Concatenate all text blocks from the assistant response."""
    parts = []
    for block in response.content:
        if hasattr(block, "text") and block.text:
            parts.append(block.text)
    return "\n".join(parts)


# ── Scout ─────────────────────────────────────────────────────────────────────
def scout(profile: str, additional_urls: str) -> str:
    """
    Call Claude with the research prompt and web search tool.
    Returns the full assistant response text.
    """
    log.info("Starting Claude web search for Tanzania opportunities...")
    prompt = PROMPT_TEMPLATE.format(
        company_profile=profile,
        additional_urls=additional_urls,
        email_address=RECIPIENT,
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=20000,
        temperature=1,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 20,
        }],
        messages=[{"role": "user", "content": prompt}],
    )

    log.info(f"Claude response: stop_reason={response.stop_reason}, "
             f"input_tokens={response.usage.input_tokens}, "
             f"output_tokens={response.usage.output_tokens}")
    return _get_full_text(response)


# ── CSV output ────────────────────────────────────────────────────────────────
def save_csv(csv_content: str, path: Path) -> None:
    path.write_text(csv_content, encoding="utf-8")
    log.info(f"CSV saved → {path}")


# ── Emailer ───────────────────────────────────────────────────────────────────
def _md_to_html(text: str) -> str:
    """Convert basic markdown (bold, bullet lists, line breaks) to HTML and escape all entities."""
    escaped = html.escape(text)
    # Bold: **text** or *text*
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*",     r"<em>\1</em>", escaped)
    # Numbered / bullet list items — each becomes an <li>
    lines = escaped.splitlines()
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if re.match(r"^(\d+\.|[-•*])\s+", stripped):
            if not in_list:
                html_lines.append("<ul style='margin:6px 0;padding-left:20px;'>")
                in_list = True
            item = re.sub(r"^(\d+\.|[-•*])\s+", "", stripped)
            html_lines.append(f"  <li style='margin:3px 0;'>{item}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if stripped:
                html_lines.append(f"<p style='margin:4px 0;'>{line}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def _build_email_body(summary: str, key_findings: str, opp_count: str) -> str:
    """Return a self-contained HTML email string."""
    date_str      = html.escape(datetime.now().strftime("%d %B %Y"))
    count_escaped = html.escape(opp_count.strip())
    summary_html  = _md_to_html(summary)
    findings_html = _md_to_html(key_findings)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>BSA Weekly Opportunities</title>
</head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,Helvetica,sans-serif;color:#222;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:24px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:8px;overflow:hidden;
                    box-shadow:0 2px 8px rgba(0,0,0,.08);">

        <!-- Header -->
        <tr>
          <td style="background:#1a3a5c;padding:28px 32px;">
            <p style="margin:0;font-size:11px;color:#8ab4d8;letter-spacing:1px;text-transform:uppercase;">
              AfroPavo Analytics
            </p>
            <h1 style="margin:6px 0 0;font-size:22px;color:#ffffff;font-weight:700;">
              Weekly Opportunity Scout
            </h1>
            <p style="margin:4px 0 0;font-size:13px;color:#a8c8e8;">{date_str}</p>
          </td>
        </tr>

        <!-- Summary banner -->
        <tr>
          <td style="background:#e8f0fe;padding:16px 32px;border-bottom:1px solid #d0ddf5;">
            <p style="margin:0;font-size:14px;color:#1a3a5c;">
              Your weekly Tanzania consulting opportunity scan is complete.
            </p>
            <p style="margin:8px 0 0;font-size:22px;font-weight:700;color:#1a3a5c;">
              {count_escaped}
              <span style="font-size:14px;font-weight:400;color:#555;"> opportunities found</span>
            </p>
          </td>
        </tr>

        <!-- Key Findings -->
        <tr>
          <td style="padding:24px 32px 12px;">
            <h2 style="margin:0 0 12px;font-size:15px;font-weight:700;color:#1a3a5c;
                        text-transform:uppercase;letter-spacing:.5px;
                        border-bottom:2px solid #1a3a5c;padding-bottom:6px;">
              Key Findings
            </h2>
            <div style="font-size:14px;line-height:1.7;color:#333;">
              {findings_html}
            </div>
          </td>
        </tr>

        <!-- Search Summary -->
        <tr>
          <td style="padding:12px 32px 24px;">
            <h2 style="margin:0 0 12px;font-size:15px;font-weight:700;color:#1a3a5c;
                        text-transform:uppercase;letter-spacing:.5px;
                        border-bottom:2px solid #e0e0e0;padding-bottom:6px;">
              Search Summary
            </h2>
            <div style="font-size:13px;line-height:1.7;color:#555;">
              {summary_html}
            </div>
          </td>
        </tr>

        <!-- Attachment note -->
        <tr>
          <td style="padding:0 32px 24px;">
            <p style="margin:0;padding:14px 18px;background:#f0f7ee;border-left:4px solid #2e7d32;
                       border-radius:4px;font-size:13px;color:#2e7d32;">
              &#128206; Full details including deadlines, budgets, eligibility, and direct links
              are in the attached CSV file.
            </p>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f8f9fa;padding:16px 32px;border-top:1px solid #e0e0e0;">
            <p style="margin:0;font-size:12px;color:#888;text-align:center;">
              BSA Opportunity Scout &nbsp;|&nbsp; AfroPavo Analytics &nbsp;|&nbsp;
              <a href="https://www.afropavoanalytics.com" style="color:#1a3a5c;text-decoration:none;">
                afropavoanalytics.com
              </a>
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_email(csv_path: Path, summary: str, key_findings: str, opp_count: str) -> bool:
    """Send the weekly report email with CSV attachment. Returns True on success."""
    if not SENDER_EMAIL or not SENDER_PASS:
        log.warning("Email credentials not set (SENDER_EMAIL / SENDER_APP_PASSWORD) — skipping email")
        return False

    # Sanitise opp_count for Subject: extract just the number from any markdown/multiline text.
    count_clean = re.sub(r"[^\d]", "", opp_count.split("\n")[0]) or opp_count.split("\n")[0][:20]

    html_body = _build_email_body(summary, key_findings, opp_count)

    msg           = MIMEMultipart("mixed")
    msg["From"]   = SENDER_EMAIL
    msg["To"]     = RECIPIENT
    msg["Subject"] = (
        f"BSA Weekly Opportunities - {datetime.now().strftime('%d %b %Y')} "
        f"({count_clean} found)"
    )
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with open(csv_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{csv_path.name}"')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(SENDER_EMAIL, SENDER_PASS)
            s.sendmail(SENDER_EMAIL, RECIPIENT, msg.as_string())
        log.info(f"Email sent to {RECIPIENT}")
        return True

    except smtplib.SMTPAuthenticationError:
        log.error("SMTP auth failed — check SENDER_EMAIL and SENDER_APP_PASSWORD (use Gmail App Password)")
        return False
    except smtplib.SMTPException as e:
        log.error(f"SMTP error: {e}")
        return False
    except OSError as e:
        log.error(f"Network error connecting to SMTP: {e}")
        return False


# ── Main pipeline ─────────────────────────────────────────────────────────────
def main() -> int:
    """
    Full pipeline. Returns exit code:
      0 = success  |  1 = no CSV extracted  |  2 = profile load failure
    """
    log.info("=== BSA Opportunity Scout starting ===")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load inputs
    try:
        profile = load_profile()
        log.info("Company profile loaded.")
    except (FileNotFoundError, ValueError) as e:
        log.error(f"Cannot load company profile: {e}")
        return 2

    additional_urls = load_additional_urls()

    # Run Claude web search
    try:
        response_text = scout(profile, additional_urls)
    except anthropic.APIConnectionError as e:
        log.error(f"Claude API connection error: {e}")
        return 1
    except anthropic.APIStatusError as e:
        log.error(f"Claude API error (HTTP {e.status_code}): {e.message}")
        return 1

    # Extract sections
    csv_content  = extract_section(response_text, "csv_data")
    summary      = extract_section(response_text, "search_summary")
    key_findings = extract_section(response_text, "key_findings")
    opp_count    = extract_section(response_text, "opportunities_found")

    if not csv_content:
        log.error("No <csv_data> section found in Claude response — cannot save report")
        # Save raw response for debugging
        debug_path = OUTPUT_DIR / f"debug_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        debug_path.write_text(response_text, encoding="utf-8")
        log.info(f"Raw response saved for debugging → {debug_path}")
        return 1

    # Save CSV
    date_str  = datetime.now().strftime("%Y%m%d")
    csv_path  = OUTPUT_DIR / f"BSA_Opportunities_{date_str}.csv"
    save_csv(csv_content, csv_path)

    # Send email
    send_email(csv_path, summary, key_findings, opp_count)

    log.info(f"=== Done === | {opp_count} opportunities | CSV: {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
