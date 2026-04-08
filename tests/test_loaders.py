"""
Tests for file loaders: load_profile() and load_additional_urls().
"""
import pytest
import main as m


class TestLoadProfile:
    def test_loads_profile_text(self, tmp_path, monkeypatch):
        profile_file = tmp_path / "company_profile.txt"
        profile_file.write_text("AfroPavo Analytics profile text", encoding="utf-8")
        monkeypatch.setattr(m, "COMPANY_PROFILE", profile_file)

        result = m.load_profile()
        assert result == "AfroPavo Analytics profile text"

    def test_raises_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(m, "COMPANY_PROFILE", tmp_path / "nonexistent.txt")
        with pytest.raises(FileNotFoundError):
            m.load_profile()

    def test_raises_when_file_is_empty(self, tmp_path, monkeypatch):
        empty_file = tmp_path / "company_profile.txt"
        empty_file.write_text("", encoding="utf-8")
        monkeypatch.setattr(m, "COMPANY_PROFILE", empty_file)
        with pytest.raises(ValueError, match="empty"):
            m.load_profile()

    def test_strips_whitespace(self, tmp_path, monkeypatch):
        profile_file = tmp_path / "company_profile.txt"
        profile_file.write_text("  Some profile text  \n\n", encoding="utf-8")
        monkeypatch.setattr(m, "COMPANY_PROFILE", profile_file)

        result = m.load_profile()
        assert result == "Some profile text"


class TestLoadAdditionalUrls:
    def test_loads_urls(self, tmp_path, monkeypatch):
        urls_file = tmp_path / "additional_urls.txt"
        urls_file.write_text("https://example.com\nhttps://another.com", encoding="utf-8")
        monkeypatch.setattr(m, "ADDITIONAL_URLS", urls_file)

        result = m.load_additional_urls()
        assert "https://example.com" in result
        assert "https://another.com" in result

    def test_returns_empty_string_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(m, "ADDITIONAL_URLS", tmp_path / "nonexistent.txt")

        result = m.load_additional_urls()
        assert result == ""
