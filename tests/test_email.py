"""
Tests for email building and sending.
"""
import smtplib
from unittest.mock import MagicMock, patch

import pytest

import main as m


@pytest.fixture(autouse=True)
def patch_credentials(monkeypatch):
    monkeypatch.setattr(m, "SENDER_EMAIL", "sender@gmail.com")
    monkeypatch.setattr(m, "SENDER_PASS", "app-password-here")


class TestBuildEmailBody:
    def test_contains_opportunity_count(self):
        body = m._build_email_body("Sources searched.", "1. FSDT RFP", "7")
        assert "7" in body

    def test_contains_key_findings(self):
        body = m._build_email_body("Summary.", "Top finding: FSDT", "3")
        assert "Top finding: FSDT" in body

    def test_contains_search_summary(self):
        body = m._build_email_body("Searched 14 portals.", "Finding 1", "5")
        assert "Searched 14 portals." in body

    def test_greets_alex(self):
        body = m._build_email_body("Summary.", "Findings.", "2")
        assert "Alex" in body


class TestSendEmail:
    def test_returns_true_on_success(self, tmp_output):
        csv_path = tmp_output / "report.csv"
        csv_path.write_text("col1,col2\nval1,val2")

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__ = MagicMock(return_value=False)

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            result = m.send_email(csv_path, "summary", "findings", "3")

        assert result is True
        mock_smtp.login.assert_called_once_with("sender@gmail.com", "app-password-here")
        mock_smtp.sendmail.assert_called_once()

    def test_csv_file_attached(self, tmp_output):
        csv_path = tmp_output / "report.csv"
        csv_path.write_text("col1,col2\nval1,val2")

        captured = {}

        def fake_sendmail(from_addr, to_addr, msg_str):
            captured["raw"] = msg_str

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__ = MagicMock(return_value=False)
        mock_smtp.sendmail.side_effect = fake_sendmail

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            m.send_email(csv_path, "summary", "findings", "3")

        assert csv_path.name in captured.get("raw", "")

    def test_returns_false_when_credentials_not_set(self, tmp_output, monkeypatch):
        monkeypatch.setattr(m, "SENDER_EMAIL", None)
        monkeypatch.setattr(m, "SENDER_PASS", None)
        csv_path = tmp_output / "report.csv"
        csv_path.write_text("col1,col2\nval1,val2")

        result = m.send_email(csv_path, "summary", "findings", "3")
        assert result is False

    def test_returns_false_on_auth_error(self, tmp_output):
        csv_path = tmp_output / "report.csv"
        csv_path.write_text("col1,col2\nval1,val2")

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__ = MagicMock(return_value=False)
        mock_smtp.login.side_effect = smtplib.SMTPAuthenticationError(535, b"auth failed")

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            result = m.send_email(csv_path, "summary", "findings", "3")

        assert result is False

    def test_returns_false_on_smtp_error(self, tmp_output):
        csv_path = tmp_output / "report.csv"
        csv_path.write_text("col1,col2\nval1,val2")

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__ = MagicMock(return_value=False)
        mock_smtp.login.side_effect = smtplib.SMTPException("server unavailable")

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            result = m.send_email(csv_path, "summary", "findings", "3")

        assert result is False

    def test_returns_false_on_network_error(self, tmp_output):
        csv_path = tmp_output / "report.csv"
        csv_path.write_text("col1,col2\nval1,val2")

        with patch("main.smtplib.SMTP_SSL", side_effect=OSError("connection refused")):
            result = m.send_email(csv_path, "summary", "findings", "3")

        assert result is False
