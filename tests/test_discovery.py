"""
Tests for discover_sources(): local model integration, deduplication,
malformed responses, and graceful failure handling.
"""
import json
from unittest.mock import MagicMock

import pytest

import main as m


def _mock_ollama(text: str):
    """Build a mock ollama.chat return value containing `text`."""
    resp = MagicMock()
    resp.message.content = text
    return resp


NEW_SITES_JSON = json.dumps([
    {"name": "UNDP Tanzania",  "url": "https://procurement.undp.org/tz",  "country_filter": None},
    {"name": "PPRA Tanzania",  "url": "https://www.ppra.go.tz/tenders",   "country_filter": None},
])


class TestDiscoverSources:
    def test_returns_new_sites(self, sample_profile, monkeypatch):
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama(NEW_SITES_JSON))
        existing = {"https://www.ungm.org/Public/Notice"}

        result = m.discover_sources(sample_profile, existing)

        assert len(result) == 2
        names = [s["name"] for s in result]
        assert "UNDP Tanzania" in names
        assert "PPRA Tanzania" in names

    def test_deduplicates_existing_urls(self, sample_profile, monkeypatch):
        sites_with_duplicate = json.dumps([
            {"name": "UNGM",          "url": "https://www.ungm.org/Public/Notice",  "country_filter": None},
            {"name": "PPRA Tanzania", "url": "https://www.ppra.go.tz/tenders",      "country_filter": None},
        ])
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama(sites_with_duplicate))
        existing = {"https://www.ungm.org/Public/Notice"}

        result = m.discover_sources(sample_profile, existing)

        assert len(result) == 1
        assert result[0]["name"] == "PPRA Tanzania"

    def test_sets_use_playwright_for_js_heavy_domains(self, sample_profile, monkeypatch):
        sites_json = json.dumps([
            {"name": "UNDP",    "url": "https://procurement.undp.org/tz", "country_filter": None},
            {"name": "Simple",  "url": "https://simple.org/tenders",      "country_filter": None},
        ])
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama(sites_json))

        result = m.discover_sources(sample_profile, set())

        undp   = next(s for s in result if s["name"] == "UNDP")
        simple = next(s for s in result if s["name"] == "Simple")
        assert undp["use_playwright"]   is True
        assert simple["use_playwright"] is False

    def test_returns_empty_on_model_exception(self, sample_profile, monkeypatch):
        def raise_err(**kwargs):
            raise OSError("ollama server not running")

        monkeypatch.setattr(m.ollama, "chat", raise_err)

        result = m.discover_sources(sample_profile, set())
        assert result == []

    def test_returns_empty_on_empty_response(self, sample_profile, monkeypatch):
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama(""))

        result = m.discover_sources(sample_profile, set())
        assert result == []

    def test_returns_empty_when_no_json_array_in_response(self, sample_profile, monkeypatch):
        monkeypatch.setattr(
            m.ollama, "chat",
            lambda **kwargs: _mock_ollama("I could not find relevant portals right now."),
        )
        result = m.discover_sources(sample_profile, set())
        assert result == []

    def test_skips_entries_missing_url(self, sample_profile, monkeypatch):
        bad_json = json.dumps([
            {"name": "No URL site"},
            {"name": "Good site", "url": "https://good.org/tenders", "country_filter": None},
        ])
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama(bad_json))

        result = m.discover_sources(sample_profile, set())
        assert len(result) == 1
        assert result[0]["name"] == "Good site"

    def test_strips_markdown_fences_from_response(self, sample_profile, monkeypatch):
        wrapped = f"```json\n{NEW_SITES_JSON}\n```"
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama(wrapped))

        result = m.discover_sources(sample_profile, set())
        assert len(result) == 2

    def test_returns_empty_on_malformed_json(self, sample_profile, monkeypatch):
        monkeypatch.setattr(m.ollama, "chat", lambda **kwargs: _mock_ollama("[{invalid json}]"))
        result = m.discover_sources(sample_profile, set())
        assert result == []
