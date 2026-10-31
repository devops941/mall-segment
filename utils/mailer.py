"""SMTP delivery for store credentials and admin notifications."""

from __future__ import annotations

import os
import pathlib
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).resolve().parent.parent / ".env")

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM") or SMTP_USER
FROM_NAME = os.getenv("FROM_NAME", "Mall Segment")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


def is_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASS)


def send_email(to_email: str, subject: str, body: str) -> tuple[bool, str]:
    """Send a plain-text email. Returns (ok, message) instead of raising."""
    if not is_configured():
        return False, "SMTP is not configured."
    if not to_email:
        return False, "No recipient address."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{SMTP_FROM}>"
    msg["To"] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, "sent"
    except Exception as exc:  # noqa: BLE001 - surfaced to the admin UI
        return False, f"{type(exc).__name__}: {exc}"


def send_store_credentials(
    to_email: str, store_name: str, password: str, login_url: str = "http://localhost:8501"
) -> tuple[bool, str]:
    body = (
        f"Hello {store_name},\n\n"
        f"Your mall analytics store account is ready.\n\n"
        f"Login URL: {login_url}\n"
        f"Email: {to_email}\n"
        f"Temporary password: {password}\n\n"
        f"Please sign in and keep these credentials safe.\n\n"
        f"— {FROM_NAME}"
    )
    return send_email(to_email, "Your Mall Segment store credentials", body)


def notify_admin_new_store(store_name: str, store_email: str) -> tuple[bool, str]:
    if not ADMIN_EMAIL:
        return False, "ADMIN_EMAIL is not configured."
    body = (
        f"A new store has registered and is awaiting approval.\n\n"
        f"Store: {store_name}\n"
        f"Email: {store_email}\n\n"
        f"Sign in as admin to approve or reject this request.\n\n"
        f"— {FROM_NAME}"
    )
    return send_email(ADMIN_EMAIL, "New store registration pending approval", body)


def notify_store_approved(to_email: str, store_name: str) -> tuple[bool, str]:
    body = (
        f"Hello {store_name},\n\n"
        f"Your store account has been approved. You can now sign in and start "
        f"entering customer data.\n\n"
        f"— {FROM_NAME}"
    )
    return send_email(to_email, "Your store account was approved", body)
