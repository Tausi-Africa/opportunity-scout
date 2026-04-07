"""
Tests for the local model fit assessment: assess() and _validate_assessment().
"""
import json
from unittest.mock import MagicMock

import pytest

import main as m


def _make_ollama_response(text: str):
    """Build a minimal mock Ollama response containing `text`."""
    resp = MagicMock()
    resp.message.content = text
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
        monkeypatch.setattr(
            m.ollama, "chat",
            lambda **kwargs: _make_ollama_response(json.dumps(sample_assessment)),
        )

        result = m.assess(sample_opportunity, sample_profile)

        assert result is not None
        assert result["fit_assessment"] == "fit"
        assert result["source_url"] == sample_opportunity["source_url"]
        assert result["source"] == sample_opportunity["source"]

    def test_strips_markdown_fences(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        wrapped = f"```json\n{json.dumps(sample_assessment)}\n```"
        monkeypatch.setattr(
            m.ollama, "chat",
            lambda **kwargs: _make_ollama_response(wrapped),
        )

        result = m.assess(sample_opportunity, sample_profile)
        assert result is not None
        assert result["fit_assessment"] == "fit"

    def test_returns_none_on_invalid_json(
        self, sample_opportunity, sample_profile, monkeypatch
    ):
        monkeypatch.setattr(
            m.ollama, "chat",
            lambda **kwargs: _make_ollama_response("Sorry, I cannot assess this right now."),
        )

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_missing_required_keys(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        del sample_assessment["fit_assessment"]
        monkeypatch.setattr(
            m.ollama, "chat",
            lambda **kwargs: _make_ollama_response(json.dumps(sample_assessment)),
        )

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_model_exception(
        self, sample_opportunity, sample_profile, monkeypatch
    ):
        def raise_err(**kwargs):
            raise ConnectionError("connection refused to ollama server")

        monkeypatch.setattr(m.ollama, "chat", raise_err)

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None

    def test_returns_none_on_invalid_fit_value(
        self, sample_opportunity, sample_assessment, sample_profile, monkeypatch
    ):
        sample_assessment["fit_assessment"] = "unknown_value"
        monkeypatch.setattr(
            m.ollama, "chat",
            lambda **kwargs: _make_ollama_response(json.dumps(sample_assessment)),
        )

        result = m.assess(sample_opportunity, sample_profile)
        assert result is None
