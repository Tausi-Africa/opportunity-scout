"""
Integration tests for the main() pipeline.
Mocks Claude API and file I/O; verifies exit codes and outputs.
"""
from pathlib import Path
from unittest.mock import MagicMock, patch

import anthropic
import pytest

import main as m
from conftest import SAMPLE_RESPONSE, SAMPLE_CSV


@pytest.fixture()
def mock_profile(tmp_path, monkeypatch):
    profile_file = tmp_path / "company_profile.txt"
    profile_file.write_text("AfroPavo Analytics profile text", encoding="utf-8")
    monkeypatch.setattr(m, "COMPANY_PROFILE", profile_file)
    return profile_file


@pytest.fixture()
def mock_urls(tmp_path, monkeypatch):
    urls_file = tmp_path / "additional_urls.txt"
    urls_file.write_text("https://example.com/tenders", encoding="utf-8")
    monkeypatch.setattr(m, "ADDITIONAL_URLS", urls_file)
    return urls_file


@pytest.fixture()
def mock_output(tmp_path, monkeypatch):
    out = tmp_path / "output"
    monkeypatch.setattr(m, "OUTPUT_DIR", out)
    return out


class TestMainPipeline:
    def test_exits_2_when_profile_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(m, "COMPANY_PROFILE", tmp_path / "nonexistent.txt")
        monkeypatch.setattr(m, "OUTPUT_DIR", tmp_path / "out")
        assert m.main() == 2

    def test_returns_0_on_success(self, mock_profile, mock_urls, mock_output, monkeypatch):
        with patch("main.scout", return_value=SAMPLE_RESPONSE):
            with patch("main.send_email", return_value=True):
                result = m.main()
        assert result == 0

    def test_csv_file_is_created(self, mock_profile, mock_urls, mock_output, monkeypatch):
        with patch("main.scout", return_value=SAMPLE_RESPONSE):
            with patch("main.send_email", return_value=False):
                m.main()

        csv_files = list(mock_output.glob("*.csv"))
        assert len(csv_files) == 1
        assert "BSA_Opportunities_" in csv_files[0].name

    def test_csv_contains_extracted_data(self, mock_profile, mock_urls, mock_output, monkeypatch):
        with patch("main.scout", return_value=SAMPLE_RESPONSE):
            with patch("main.send_email", return_value=False):
                m.main()

        csv_path = next(mock_output.glob("*.csv"))
        content = csv_path.read_text(encoding="utf-8")
        assert "Opportunity_Title" in content
        assert "FSDT" in content

    def test_returns_1_when_no_csv_in_response(self, mock_profile, mock_urls, mock_output):
        response_no_csv = "<search_summary>Searched.</search_summary><opportunities_found>0</opportunities_found>"
        with patch("main.scout", return_value=response_no_csv):
            result = m.main()
        assert result == 1

    def test_debug_file_saved_when_csv_missing(self, mock_profile, mock_urls, mock_output):
        response_no_csv = "<search_summary>Searched.</search_summary>"
        with patch("main.scout", return_value=response_no_csv):
            m.main()

        debug_files = list(mock_output.glob("debug_response_*.txt"))
        assert len(debug_files) == 1

    def test_returns_1_on_api_connection_error(self, mock_profile, mock_urls, mock_output):
        with patch("main.scout", side_effect=anthropic.APIConnectionError(request=MagicMock())):
            result = m.main()
        assert result == 1

    def test_returns_1_on_api_status_error(self, mock_profile, mock_urls, mock_output):
        with patch(
            "main.scout",
            side_effect=anthropic.APIStatusError(
                message="rate limit", response=MagicMock(status_code=429), body={}
            ),
        ):
            result = m.main()
        assert result == 1
