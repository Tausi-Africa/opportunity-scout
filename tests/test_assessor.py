"""
Tests for the Claude AI fit assessment: assess() and _validate_assessment().
"""
import json
from unittest.mock import MagicMock

import anthropic
import pytest

import main as m


def _make_claude_response(text: str):
    """Build a minimal mock Claude API response containing `text`."""
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    return resp


class TestValidateAssessment:
    def test_valid_assessment_passes(self, sample_assessment):
        assert m._validate_assessment(sample_assessment) is True

    def test_missing_key_fails(self, sample_assessment):
        del sample_assessment["fit_assessment"]
        assert m._validate_assessment(sample_assessment) is False

    def test_invalid_fit_value_fails(self, sample_assessment):
        sample_assessment["fit_assessment"] = "maybe"
        assert m._validate_assessment(sample_assessment) is False

    def test_sectors_as_string_is_coerced_to_list(self, sample_assessment):
        sample_assessment["sectors"] = "Finance"
        result = m._validate_assessment(sample_assessment)
        assert result is True
        assert isinstance(sample_assessment["sectors"], list)

    def test_eligibility_as_string_is_coerced_to_list(self, sample_assessment):
        sample_assessment["eligibility"] = "Must be registered"
        result = m._validate_assessment(sample_assessment)
        assert result is True
        assert isinstance(sample_assessment["eligibility"], list)

    @pytest.mark.parametrize("fit_val", ["fit", "nearly_fit", "far_fetched"])
    def test_all_valid_fit_values_accepted(self, sample_assessment, fit_val):
        sample_assessment["fit_assessment"] = fit_val
        assert m._validate_assessment(sample_assessment) is True


class TestAssess:
    def test_returns_assessment_on_valid_response(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _make_claude_response(
            json.dumps(sample_assessment)
        )
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)

        assert result is not None
        assert result["fit_assessment"] == "fit"
        assert result["source_url"] == sample_opportunity["source_url"]
        assert result["source"] == sample_opportunity["source"]

    def test_strips_markdown_fences(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        wrapped = f"```json\n{json.dumps(sample_assessment)}\n```"
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _make_claude_response(wrapped)
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is not None
        assert result["fit_assessment"] == "fit"

    def test_returns_none_on_invalid_json(
        self, sample_opportunity, sample_profile, monkeypatch
    ):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _make_claude_response(
            "Sorry, I cannot assess this right now."
        )
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_missing_required_keys(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        del sample_assessment["fit_assessment"]
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _make_claude_response(
            json.dumps(sample_assessment)
        )
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_api_status_error(
        self, sample_opportunity, sample_profile, monkeypatch
    ):
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = anthropic.APIStatusError(
            message="rate limit", response=MagicMock(status_code=429), body={}
        )
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_connection_error(
        self, sample_opportunity, sample_profile, monkeypatch
    ):
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = anthropic.APIConnectionError(
            request=MagicMock()
        )
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_invalid_fit_value(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        sample_assessment["fit_assessment"] = "unknown_value"
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _make_claude_response(
            json.dumps(sample_assessment)
        )
        monkeypatch.setattr(m, "CLAUDE_CLIENT", mock_client)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None
