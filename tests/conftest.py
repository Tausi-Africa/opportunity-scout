"""
Shared pytest fixtures for BSA Opportunity Scout tests.
"""
import sys
from pathlib import Path

import pytest

# Make scripts/ importable without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


SAMPLE_PROFILE = (
    "AfroPavo Analytics is a Tanzanian consulting firm specialising in data analytics, "
    "AI/ML, credit risk, fintech, digital transformation, and capacity building. "
    "Clients include FSDT, Vodacom, FINCA, CRDB, Azania Bank."
)

SAMPLE_URLS = (
    "https://www.ungm.org/Public/Notice\n"
    "https://www.fsdt.or.tz/work-with-us/\n"
    "https://crdbbank.co.tz/en/about-us/tender"
)

SAMPLE_CSV = (
    "Opportunity_Title,Type,Organization,URL,Contact_Email,Contact_Phone,"
    "Contact_Person,Deadline,Qualification_Criteria,Description,Relevance_Score,Date_Found\n"
    '"Digital Finance Research","RFP","FSDT","https://fsdt.or.tz/rfp1","procurement@fsdt.or.tz",'
    '"","","2026-06-30","Data analytics expertise","Research on DFS adoption","High","2026-04-08"'
)

SAMPLE_RESPONSE = f"""
<search_summary>
Searched 14 portals including UNGM, World Bank, FSDT, and others.
</search_summary>

<opportunities_found>
12
</opportunities_found>

<key_findings>
1. FSDT Digital Finance Research - High relevance, matches core analytics capability.
2. World Bank Tanzania ICT project - Medium relevance.
</key_findings>

<csv_data>
{SAMPLE_CSV}
</csv_data>

<email_instructions>
Confirm that this CSV should be sent to alex@bsa.ai
</email_instructions>
"""


@pytest.fixture()
def sample_profile() -> str:
    return SAMPLE_PROFILE


@pytest.fixture()
def sample_urls() -> str:
    return SAMPLE_URLS


@pytest.fixture()
def sample_response() -> str:
    return SAMPLE_RESPONSE


@pytest.fixture()
def sample_csv() -> str:
    return SAMPLE_CSV


@pytest.fixture()
def tmp_output(tmp_path) -> Path:
    out = tmp_path / "output"
    out.mkdir()
    return out
