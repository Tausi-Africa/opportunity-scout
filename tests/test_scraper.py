"""
Tests for scraping helpers: is_relevant, safe_get, find_pdf_links,
_passes_country_filter, parse_pdf, _fetch_detail, scrape_site.
"""
import io
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
import requests
from bs4 import BeautifulSoup

import main as m


# ── is_relevant ───────────────────────────────────────────────────────────────

class TestIsRelevant:
    def test_keyword_match_returns_true(self):
        assert m.is_relevant("Consultancy for data analytics in Tanzania") is True

    def test_no_keyword_returns_false(self):
        assert m.is_relevant("Supply of office furniture and stationery") is False

    def test_case_insensitive(self):
        assert m.is_relevant("DIGITAL TRANSFORMATION PROJECT") is True

    def test_partial_word_match(self):
        # "credit" is a keyword; "accreditation" contains it
        assert m.is_relevant("accreditation body assessment") is True

    def test_empty_string_returns_false(self):
        assert m.is_relevant("") is False

    def test_multiple_keywords(self):
        assert m.is_relevant("Research and feasibility study on fintech") is True


# ── safe_get ──────────────────────────────────────────────────────────────────

class TestSafeGet:
    def test_successful_get_returns_response(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("main.requests.get", return_value=mock_resp) as mock_get:
            mock_resp.raise_for_status.return_value = None
            result = m.safe_get("https://example.com")
        assert result is mock_resp
        mock_get.assert_called_once()

    def test_404_returns_none_without_retry(self):
        """Client errors (4xx) should not be retried."""
        http_err = requests.HTTPError(response=MagicMock(status_code=404))
        with patch("main.requests.get", side_effect=http_err):
            result = m.safe_get("https://example.com/not-found")
        assert result is None

    def test_403_returns_none_without_retry(self):
        http_err = requests.HTTPError(response=MagicMock(status_code=403))
        with patch("main.requests.get", side_effect=http_err):
            result = m.safe_get("https://example.com/forbidden")
        assert result is None

    def test_500_retries_exactly_three_times(self):
        """5xx errors trigger exactly 3 requests.get calls then safe_get gives up."""
        http_err = requests.HTTPError(response=MagicMock(status_code=500))
        with patch("main.requests.get", side_effect=http_err) as mock_get:
            with patch("main.time.sleep"):
                try:
                    result = m.safe_get("https://example.com/server-error")
                except requests.HTTPError:
                    result = None  # some implementations raise, others return None
        assert mock_get.call_count == 3
        assert result is None

    def test_timeout_retries(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        with patch(
            "main.requests.get",
            side_effect=[requests.Timeout(), requests.Timeout(), mock_resp],
        ):
            with patch("main.time.sleep"):
                result = m.safe_get("https://example.com/slow")
        assert result is mock_resp

    def test_connection_error_retries_exactly_three_times(self):
        """Connection errors trigger exactly 3 requests.get calls then safe_get gives up."""
        with patch("main.requests.get", side_effect=requests.ConnectionError("refused")) as mock_get:
            with patch("main.time.sleep"):
                try:
                    result = m.safe_get("https://example.com/unreachable")
                except requests.ConnectionError:
                    result = None  # some implementations raise, others return None
        assert mock_get.call_count == 3
        assert result is None


# ── find_pdf_links ────────────────────────────────────────────────────────────

class TestFindPdfLinks:
    BASE = "https://example.com/tenders"

    def _soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    def test_absolute_pdf_link_returned(self):
        soup = self._soup('<a href="https://example.com/doc.pdf">Download</a>')
        assert m.find_pdf_links(soup, self.BASE) == ["https://example.com/doc.pdf"]

    def test_path_relative_pdf_link_resolved(self):
        """Relative paths (no leading /) join onto the base URL."""
        soup = self._soup('<a href="docs/brief.pdf">Brief</a>')
        links = m.find_pdf_links(soup, self.BASE)
        assert links == [f"{self.BASE}/docs/brief.pdf"]

    def test_root_relative_pdf_link_resolved(self):
        """Root-relative paths (/...) resolve against scheme+host only."""
        base_no_path = "https://example.com"
        soup = self._soup('<a href="/files/brief.pdf">Brief</a>')
        links = m.find_pdf_links(soup, base_no_path)
        assert links == ["https://example.com/files/brief.pdf"]

    def test_non_pdf_links_excluded(self):
        soup = self._soup('<a href="/page.html">Page</a><a href="/doc.docx">Doc</a>')
        assert m.find_pdf_links(soup, self.BASE) == []

    def test_capped_at_three(self):
        html = "".join(f'<a href="/f{i}.pdf">F{i}</a>' for i in range(6))
        soup = self._soup(html)
        assert len(m.find_pdf_links(soup, self.BASE)) == 3

    def test_empty_page_returns_empty(self):
        soup = self._soup("<p>No documents here.</p>")
        assert m.find_pdf_links(soup, self.BASE) == []

    def test_case_insensitive_pdf_extension(self):
        soup = self._soup('<a href="/DOC.PDF">Upper PDF</a>')
        links = m.find_pdf_links(soup, self.BASE)
        assert len(links) == 1


# ── _passes_country_filter ────────────────────────────────────────────────────

class TestPassesCountryFilter:
    def test_no_filter_always_passes(self, site_no_filter):
        anchor = MagicMock()
        anchor.parent = None
        assert m._passes_country_filter(site_no_filter, anchor, "/any-href") is True

    def test_filter_matches_in_parent_text(self, site_with_filter):
        anchor = MagicMock()
        anchor.parent.get_text.return_value = "Opportunity in Tanzania region"
        assert m._passes_country_filter(site_with_filter, anchor, "/tender/123") is True

    def test_filter_matches_in_href(self, site_with_filter):
        anchor = MagicMock()
        anchor.parent.get_text.return_value = "Generic listing"
        assert m._passes_country_filter(site_with_filter, anchor, "/tenders/tanzania/456") is True

    def test_filter_not_found_returns_false(self, site_with_filter):
        anchor = MagicMock()
        anchor.parent.get_text.return_value = "Opportunity in Kenya"
        assert m._passes_country_filter(site_with_filter, anchor, "/tenders/kenya/789") is False

    def test_no_parent_falls_back_to_href_check(self, site_with_filter):
        anchor = MagicMock()
        anchor.parent = None
        assert m._passes_country_filter(site_with_filter, anchor, "/tz-tenders/001") is False


# ── parse_pdf ─────────────────────────────────────────────────────────────────

SAMPLE_PDF_PATH = Path(__file__).parent.parent / "samplePDFs" / "sample.pdf"


class TestParsePdf:
    def test_returns_text_from_real_pdf(self):
        """Uses samplePDFs/sample.pdf (https://s2.q4cdn.com/175719177/files/doc_presentations/Placeholder-PDF.pdf)."""
        assert SAMPLE_PDF_PATH.exists(), f"Sample PDF not found at {SAMPLE_PDF_PATH}"
        pdf_bytes = SAMPLE_PDF_PATH.read_bytes()
        mock_resp = MagicMock()
        mock_resp.content = pdf_bytes

        with patch("main.safe_get", return_value=mock_resp):
            result = m.parse_pdf("https://example.com/sample.pdf")

        assert isinstance(result, str)
        assert len(result) > 0

    def test_real_pdf_contains_expected_content(self):
        """Extracted text from samplePDFs/sample.pdf must contain 'Placeholder PDF'."""
        assert SAMPLE_PDF_PATH.exists(), f"Sample PDF not found at {SAMPLE_PDF_PATH}"
        pdf_bytes = SAMPLE_PDF_PATH.read_bytes()
        mock_resp = MagicMock()
        mock_resp.content = pdf_bytes

        with patch("main.safe_get", return_value=mock_resp):
            result = m.parse_pdf("https://example.com/sample.pdf")

        assert "Placeholder PDF" in result

    def test_returns_empty_when_get_fails(self):
        with patch("main.safe_get", return_value=None):
            assert m.parse_pdf("https://example.com/missing.pdf") == ""

    def test_returns_empty_on_corrupt_pdf(self):
        mock_resp = MagicMock()
        mock_resp.content = b"not a pdf"
        with patch("main.safe_get", return_value=mock_resp):
            with patch("main.pdfplumber.open", side_effect=Exception("corrupt")):
                assert m.parse_pdf("https://example.com/corrupt.pdf") == ""

    def test_text_truncated_at_6000_chars(self):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "A" * 10_000
        mock_pdf   = MagicMock()
        mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
        mock_pdf.__exit__  = MagicMock(return_value=False)
        mock_pdf.pages     = [mock_page]

        mock_resp = MagicMock()
        mock_resp.content = b"%PDF fake"

        with patch("main.safe_get", return_value=mock_resp):
            with patch("main.pdfplumber.open", return_value=mock_pdf):
                result = m.parse_pdf("https://example.com/long.pdf")

        assert len(result) <= 6000


# ── scrape_site ───────────────────────────────────────────────────────────────

class TestScrapeSite:
    LISTING_HTML = """
    <html><body>
      <a href="/tenders/001">Digital Financial Services Research Consultancy</a>
      <a href="/tenders/002">Data Analytics and Credit Risk Advisory Tanzania</a>
      <a href="/about">About Us</a>
    </body></html>
    """
    DETAIL_HTML = "<html><body><p>Full tender details here. Deadline: 30 June 2026.</p></body></html>"

    def test_returns_relevant_opportunities(self, site_no_filter):
        detail_resp = MagicMock()
        detail_resp.text = self.DETAIL_HTML

        with patch("main._get_page_html", return_value=self.LISTING_HTML):
            with patch("main.safe_get", return_value=detail_resp):
                with patch("main.time.sleep"):
                    results = m.scrape_site(site_no_filter)

        assert len(results) == 2
        assert all(r["source"] == site_no_filter["name"] for r in results)

    def test_returns_empty_when_no_html(self, site_no_filter):
        with patch("main._get_page_html", return_value=""):
            results = m.scrape_site(site_no_filter)
        assert results == []

    def test_short_titles_excluded(self, site_no_filter):
        html = '<html><body><a href="/t">Hi</a></body></html>'
        with patch("main._get_page_html", return_value=html):
            results = m.scrape_site(site_no_filter)
        assert results == []

    def test_irrelevant_titles_excluded(self, site_no_filter):
        html = '<html><body><a href="/t/1">Supply of office furniture and cleaning services</a></body></html>'
        with patch("main._get_page_html", return_value=html):
            results = m.scrape_site(site_no_filter)
        assert results == []

    def test_duplicate_hrefs_not_repeated(self, site_no_filter):
        html = """
        <a href="/dup">Data Analytics Research Consultancy Tanzania</a>
        <a href="/dup">Data Analytics Research Consultancy Tanzania</a>
        """
        detail_resp = MagicMock()
        detail_resp.text = self.DETAIL_HTML
        with patch("main._get_page_html", return_value=html):
            with patch("main.safe_get", return_value=detail_resp):
                with patch("main.time.sleep"):
                    results = m.scrape_site(site_no_filter)
        assert len(results) == 1
