"""
Integration tests for the main() pipeline orchestration.
Mocks all external calls; verifies the pipeline wires correctly end-to-end.
"""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

import main as m


@pytest.fixture()
def mock_profile(tmp_path, monkeypatch, sample_profile):
    """Write a real company_profile.txt and point COMPANY_PROFILE at it."""
    profile_file = tmp_path / "company_profile.txt"
    profile_file.write_text(sample_profile, encoding="utf-8")
    monkeypatch.setattr(m, "COMPANY_PROFILE", profile_file)
    return profile_file


@pytest.fixture()
def mock_output(tmp_path, monkeypatch):
    out = tmp_path / "output"
    monkeypatch.setattr(m, "OUTPUT_DIR", out)
    return out


@pytest.fixture()
def mock_scraped_opps(sample_opportunity):
    return [sample_opportunity]


@pytest.fixture()
def mock_assessment(sample_assessment):
    return sample_assessment


class TestMainPipeline:
    def test_exits_2_when_profile_missing(self, monkeypatch, tmp_path):
        monkeypatch.setattr(m, "COMPANY_PROFILE", tmp_path / "nonexistent.txt")
        monkeypatch.setattr(m, "OUTPUT_DIR", tmp_path / "out")
        result = m.main()
        assert result == 2

    def test_returns_0_on_full_success(
        self, mock_profile, mock_output, mock_scraped_opps, mock_assessment, monkeypatch
    ):
        monkeypatch.setattr(m, "SITES", [
            {"name": "Test", "url": "https://test.com", "country_filter": None, "use_playwright": False}
        ])
        monkeypatch.setattr(m, "SENDER_EMAIL", "sender@gmail.com")
        monkeypatch.setattr(m, "SENDER_PASS",  "password")

        with patch("main.discover_sources", return_value=[]):
            with patch("main.scrape_site", return_value=mock_scraped_opps):
                with patch("main.assess", return_value=mock_assessment):
                    with patch("main.send_email", return_value=True):
                        with patch("main.time.sleep"):
                            result = m.main()

        assert result == 0

    def test_excel_file_is_created(
        self, mock_profile, mock_output, mock_scraped_opps, mock_assessment, monkeypatch
    ):
        monkeypatch.setattr(m, "SITES", [
            {"name": "Test", "url": "https://test.com", "country_filter": None, "use_playwright": False}
        ])

        with patch("main.discover_sources", return_value=[]):
            with patch("main.scrape_site", return_value=mock_scraped_opps):
                with patch("main.assess", return_value=mock_assessment):
                    with patch("main.send_email", return_value=False):
                        with patch("main.time.sleep"):
                            m.main()

        xlsx_files = list(mock_output.glob("*.xlsx"))
        assert len(xlsx_files) == 1

    def test_returns_1_when_no_assessments_pass(
        self, mock_profile, mock_output, mock_scraped_opps, monkeypatch
    ):
        monkeypatch.setattr(m, "SITES", [
            {"name": "Test", "url": "https://test.com", "country_filter": None, "use_playwright": False}
        ])

        with patch("main.discover_sources", return_value=[]):
            with patch("main.scrape_site", return_value=mock_scraped_opps):
                with patch("main.assess", return_value=None):   # every assessment fails
                    with patch("main.time.sleep"):
                        result = m.main()

        assert result == 1

    def test_site_failure_does_not_stop_pipeline(
        self, mock_profile, mock_output, mock_assessment, monkeypatch
    ):
        sites = [
            {"name": "Broken",  "url": "https://broken.com",  "country_filter": None, "use_playwright": False},
            {"name": "Working", "url": "https://working.com", "country_filter": None, "use_playwright": False},
        ]
        monkeypatch.setattr(m, "SITES", sites)

        working_opp = {
            "source": "Working", "source_url": "https://working.com/t/1",
            "title": "Digital Financial Research Consultancy Tanzania",
            "raw_text": "Details here.",
        }

        def side_effect(site):
            if site["name"] == "Broken":
                raise RuntimeError("connection refused")
            return [working_opp]

        with patch("main.discover_sources", return_value=[]):
            with patch("main.scrape_site", side_effect=side_effect):
                with patch("main.assess", return_value=mock_assessment):
                    with patch("main.send_email", return_value=True):
                        with patch("main.time.sleep"):
                            result = m.main()

        assert result == 0

    def test_discovered_sources_added_to_scrape_list(
        self, mock_profile, mock_output, mock_assessment, monkeypatch
    ):
        monkeypatch.setattr(m, "SITES", [])
        new_site = {"name": "Claude-Found", "url": "https://new.com/tenders",
                    "country_filter": None, "use_playwright": False}
        scraped_opp = {
            "source": "Claude-Found", "source_url": "https://new.com/tenders/1",
            "title": "Data Analytics Consultancy for Financial Services Tanzania",
            "raw_text": "Scope of work details.",
        }

        with patch("main.discover_sources", return_value=[new_site]) as mock_disc:
            with patch("main.scrape_site", return_value=[scraped_opp]) as mock_scrape:
                with patch("main.assess", return_value=mock_assessment):
                    with patch("main.send_email", return_value=True):
                        with patch("main.time.sleep"):
                            m.main()

        scraped_names = [call.args[0]["name"] for call in mock_scrape.call_args_list]
        assert "Claude-Found" in scraped_names

    def test_deduplication_removes_duplicate_titles(
        self, mock_profile, mock_output, mock_assessment, monkeypatch
    ):
        monkeypatch.setattr(m, "SITES", [
            {"name": "S1", "url": "https://s1.com", "country_filter": None, "use_playwright": False},
            {"name": "S2", "url": "https://s2.com", "country_filter": None, "use_playwright": False},
        ])
        same_opp = {
            "source": "S1", "source_url": "https://s1.com/t",
            "title": "Digital Credit Risk Consultancy Tanzania",
            "raw_text": "Details.",
        }

        with patch("main.discover_sources", return_value=[]):
            with patch("main.scrape_site", return_value=[same_opp]):
                with patch("main.assess", return_value=mock_assessment) as mock_assess:
                    with patch("main.send_email", return_value=True):
                        with patch("main.time.sleep"):
                            m.main()

        # Two sites each return the same title → should only be assessed once
        assert mock_assess.call_count == 1
