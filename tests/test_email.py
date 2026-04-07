"""
Tests for send_email(): success path, auth failure, SMTP errors, fallback file.
"""
import smtplib
from email.header import decode_header as _decode_header
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

import pytest

import main as m


def _opps(fit_count: int = 2, near_count: int = 1, far_count: int = 1) -> list[dict]:
    def _o(fit):
        return {
            "title": f"Opp ({fit})", "organization": "Org",
            "deadline": "30 June 2026", "budget": "USD 50,000",
            "fit_assessment": fit,
        }
    return (
        [_o("fit")] * fit_count
        + [_o("nearly_fit")] * near_count
        + [_o("far_fetched")] * far_count
    )


@pytest.fixture(autouse=True)
def patch_credentials(monkeypatch):
    monkeypatch.setattr(m, "SENDER_EMAIL", "sender@gmail.com")
    monkeypatch.setattr(m, "SENDER_PASS",  "app-password-here")


class TestSendEmail:
    def test_returns_true_on_success(self, tmp_output):
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__  = MagicMock(return_value=False)

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            result = m.send_email(excel, _opps())

        assert result is True
        mock_smtp.login.assert_called_once_with("sender@gmail.com", "app-password-here")
        mock_smtp.sendmail.assert_called_once()

    def test_subject_contains_strong_fit_count(self, tmp_output):
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        captured_subject = {}

        def fake_sendmail(from_addr, to_addr, msg_str):
            for line in msg_str.splitlines():
                if line.startswith("Subject:"):
                    captured_subject["subject"] = line
                    break

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__  = MagicMock(return_value=False)
        mock_smtp.sendmail.side_effect = fake_sendmail

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            m.send_email(excel, _opps(fit_count=3))

        # Subject may be RFC 2047 encoded (e.g. em-dash triggers quoted-printable).
        # Decode all parts before asserting.
        raw = captured_subject.get("subject", "").replace("Subject: ", "", 1)
        decoded = "".join(
            part.decode(enc or "utf-8") if isinstance(part, bytes) else part
            for part, enc in _decode_header(raw)
        )
        assert "3 Strong Fit" in decoded

    def test_returns_false_and_saves_fallback_on_auth_error(self, tmp_output):
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__  = MagicMock(return_value=False)
        mock_smtp.login.side_effect = smtplib.SMTPAuthenticationError(535, b"auth failed")

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            result = m.send_email(excel, _opps())

        assert result is False
        # Fallback file should be written next to the Excel
        fallback = excel.with_suffix(".email_body.txt")
        assert fallback.exists()

    def test_returns_false_on_generic_smtp_error(self, tmp_output):
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__  = MagicMock(return_value=False)
        mock_smtp.login.side_effect = smtplib.SMTPException("server unavailable")

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            result = m.send_email(excel, _opps())

        assert result is False

    def test_returns_false_on_network_error(self, tmp_output):
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        with patch("main.smtplib.SMTP_SSL", side_effect=OSError("connection refused")):
            result = m.send_email(excel, _opps())

        assert result is False

    def test_returns_false_when_credentials_not_set(self, tmp_output, monkeypatch):
        monkeypatch.setattr(m, "SENDER_EMAIL", None)
        monkeypatch.setattr(m, "SENDER_PASS",  None)
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        result = m.send_email(excel, _opps())
        assert result is False

    def test_excel_file_attached(self, tmp_output):
        excel = tmp_output / "report.xlsx"
        excel.write_bytes(b"fake xlsx content")

        captured_msg = {}

        def fake_sendmail(from_addr, to_addr, msg_str):
            captured_msg["raw"] = msg_str

        mock_smtp = MagicMock()
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__  = MagicMock(return_value=False)
        mock_smtp.sendmail.side_effect = fake_sendmail

        with patch("main.smtplib.SMTP_SSL", return_value=mock_smtp):
            m.send_email(excel, _opps())

        assert excel.name in captured_msg.get("raw", "")
