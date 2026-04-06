"""
Shared pytest fixtures for BSA Opportunity Scout tests.
"""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Make scripts/ importable without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


# ── Re-usable data fixtures ───────────────────────────────────────────────────

@pytest.fixture()
def sample_profile() -> str:
    return (
        "AfroPavo Analytics is a Tanzanian consulting firm specialising in data analytics, "
        "AI/ML, credit risk, fintech, digital transformation, and capacity building. "
        "Clients include FSDT, Vodacom, FINCA, CRDB, Azania Bank."
    )


@pytest.fixture()
def sample_opportunity() -> dict:
    return {
        "source":     "FSDT",
        "source_url": "https://www.fsdt.or.tz/work-with-us/tender-001",
        "title":      "Consultancy for Digital Financial Services Research",
        "raw_text":   (
            "FSDT Tanzania seeks a consulting firm to conduct research on digital "
            "financial services adoption. Required: data analytics expertise, "
            "experience in financial inclusion, deadline 30 June 2026. "
            "Budget: USD 80,000. Contact: procurement@fsdt.or.tz"
        ),
    }


@pytest.fixture()
def sample_assessment() -> dict:
    return {
        "title":             "Consultancy for Digital Financial Services Research",
        "organization":      "FSDT Tanzania",
        "type":              "RFP",
        "sectors":           ["Finance", "Data Analytics"],
        "deadline":          "30 June 2026",
        "budget":            "USD 80,000",
        "budget_type":       "fixed",
        "eligibility":       ["Registered firm", "5+ years experience", "Tanzania presence"],
        "fit_assessment":    "fit",
        "fit_reasoning":     "Core services match exactly. FSDT is an existing client.",
        "contact_email":     "procurement@fsdt.or.tz",
        "application_link":  "https://www.fsdt.or.tz/work-with-us/tender-001",
        "background_context": "FSDT seeks research support on DFS adoption in Tanzania.",
        "source":            "FSDT",
        "source_url":        "https://www.fsdt.or.tz/work-with-us/tender-001",
    }


@pytest.fixture()
def site_no_filter() -> dict:
    return {"name": "Test Site", "url": "https://example.com/tenders", "country_filter": None, "use_playwright": False}


@pytest.fixture()
def site_with_filter() -> dict:
    return {"name": "UNGM", "url": "https://www.ungm.org/Public/Notice", "country_filter": "Tanzania", "use_playwright": False}


@pytest.fixture()
def mock_claude_client(monkeypatch, sample_assessment):
    """Patch CLAUDE_CLIENT.messages.create to return a valid assessment JSON."""
    import main as m

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(sample_assessment))]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response
    monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)
    return mock_client


@pytest.fixture()
def tmp_output(tmp_path) -> Path:
    """A temporary output directory."""
    out = tmp_path / "output"
    out.mkdir()
    return out
