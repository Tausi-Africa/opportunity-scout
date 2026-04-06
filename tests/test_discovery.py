"""
Tests for discover_sources(): Claude web search integration, deduplication,
malformed responses, and graceful failure handling.
"""
import json
from unittest.mock import MagicMock

import pytest

import main as m


def _mock_claude(text: str):
    """Build a mock CLAUDE_CLIENT whose messages.create returns the given text."""
    block   = MagicMock()
    block.text = text
    resp    = MagicMock()
    resp.content = [block]
    client  = MagicMock()
    client.messages.create.return_value = resp
    return client


NEW_SITES_JSON = json.dumps([
    {"name": "UNDP Tanzania",  "url": "https://procurement.undp.org/tz",  "country_filter": None},
    {"name": "PPRA Tanzania",  "url": "https://www.ppra.go.tz/tenders",   "country_filter": None},
])


class TestDiscoverSources:
    def test_returns_new_sites(self, sample_profile, monkeypatch):
        monkeypatch.setattr(m, "CLAUDE_CLIENT", _mock_claude(NEW_SITES_JSON))
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
        monkeypatch.setattr(m, "CLAUDE_CLIENT", _mock_claude(sites_with_duplicate))
        existing = {"https://www.ungm.org/Public/Notice"}

        result = m.discover_sources(sample_profile, existing)

        assert len(result) == 1
        assert result[0]["name"] == "PPRA Tanzania"

    def test_sets_use_playwright_for_js_heavy_domains(self, sample_profile, monkeypatch):
        sites_json = json.dumps([
            {"name": "UNDP",    "url": "https://procurement.undp.org/tz", "country_filter": None},
            {"name": "Simple",  "url": "https://simple.org/tenders",      "country_filter": None},
        ])
        monkeypatch.setattr(m, "CLAUDE_CLIENT", _mock_claude(sites_json))

        result = m.discover_sources(sample_profile, set())

        undp   = next(s for s in result if s["name"] == "UNDP")
        simple = next(s for s in result if s["name"] == "Simple")
        assert undp["use_playwright"]   is True
        assert simple["use_playwright"] is False

    def test_returns_empty_on_api_exception(self, sample_profile, monkeypatch):
        client = MagicMock()
        client.messages.create.side_effect = Exception("network error")
        monkeypatch.setattr(m, "CLAUDE_CLIENT", client)

        result = m.discover_sources(sample_profile, set())
        assert result == []

    def test_returns_empty_on_no_text_in_response(self, sample_profile, monkeypatch):
        block      = MagicMock(spec=[])   # no .text attribute
        resp       = MagicMock()
        resp.content = [block]
        client     = MagicMock()
        client.messages.create.return_value = resp
        monkeypatch.setattr(m, "CLAUDE_CLIENT", client)

        result = m.discover_sources(sample_profile, set())
        assert result == []

    def test_returns_empty_when_no_json_array_in_response(self, sample_profile, monkeypatch):
        monkeypatch.setattr(
            m, "CLAUDE_CLIENT",
            _mock_claude("I searched the web but could not find relevant portals right now.")
        )
        result = m.discover_sources(sample_profile, set())
        assert result == []

    def test_skips_entries_missing_url(self, sample_profile, monkeypatch):
        bad_json = json.dumps([
            {"name": "No URL site"},
            {"name": "Good site", "url": "https://good.org/tenders", "country_filter": None},
        ])
        monkeypatch.setattr(m, "CLAUDE_CLIENT", _mock_claude(bad_json))

        result = m.discover_sources(sample_profile, set())
        assert len(result) == 1
        assert result[0]["name"] == "Good site"

    def test_strips_markdown_fences_from_response(self, sample_profile, monkeypatch):
        wrapped = f"```json\n{NEW_SITES_JSON}\n```"
        monkeypatch.setattr(m, "CLAUDE_CLIENT", _mock_claude(wrapped))

        result = m.discover_sources(sample_profile, set())
        assert len(result) == 2

    def test_returns_empty_on_malformed_json(self, sample_profile, monkeypatch):
        monkeypatch.setattr(m, "CLAUDE_CLIENT", _mock_claude("[{invalid json}]"))
        result = m.discover_sources(sample_profile, set())
        assert result == []
