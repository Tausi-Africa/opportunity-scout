"""
Tests for extract_section() and _get_full_text() response parsing helpers.
"""
from unittest.mock import MagicMock

import main as m
from conftest import SAMPLE_RESPONSE


class TestExtractSection:
    def test_extracts_csv_data(self):
        result = m.extract_section(SAMPLE_RESPONSE, "csv_data")
        assert "Opportunity_Title" in result
        assert "FSDT" in result

    def test_extracts_search_summary(self):
        result = m.extract_section(SAMPLE_RESPONSE, "search_summary")
        assert "Searched" in result
        assert "portals" in result

    def test_extracts_opportunities_found(self):
        result = m.extract_section(SAMPLE_RESPONSE, "opportunities_found")
        assert result == "12"

    def test_extracts_key_findings(self):
        result = m.extract_section(SAMPLE_RESPONSE, "key_findings")
        assert "FSDT" in result

    def test_returns_empty_when_tag_missing(self):
        result = m.extract_section("No tags here", "csv_data")
        assert result == ""

    def test_strips_surrounding_whitespace(self):
        text = "<tag>  hello world  </tag>"
        result = m.extract_section(text, "tag")
        assert result == "hello world"

    def test_handles_multiline_content(self):
        text = "<csv_data>\nline1\nline2\nline3\n</csv_data>"
        result = m.extract_section(text, "csv_data")
        assert "line1" in result
        assert "line2" in result
        assert "line3" in result


class TestGetFullText:
    def test_concatenates_text_blocks(self):
        block1 = MagicMock()
        block1.text = "Hello "
        block2 = MagicMock()
        block2.text = "world"

        response = MagicMock()
        response.content = [block1, block2]

        result = m._get_full_text(response)
        assert "Hello" in result
        assert "world" in result

    def test_skips_blocks_without_text(self):
        text_block = MagicMock()
        text_block.text = "actual text"
        tool_block = MagicMock(spec=[])   # no .text attribute

        response = MagicMock()
        response.content = [tool_block, text_block]

        result = m._get_full_text(response)
        assert "actual text" in result

    def test_returns_empty_for_no_text_blocks(self):
        tool_block = MagicMock(spec=[])
        response = MagicMock()
        response.content = [tool_block]

        result = m._get_full_text(response)
        assert result == ""
