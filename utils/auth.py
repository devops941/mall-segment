"""Authentication helpers: password hashing, JWT tokens, and the admin check."""

from __future__ import annotations

import hmac
import os
import pathlib
import secrets
import string
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).resolve().parent.parent / ".env")

JWT_SECRET = os.getenv("JWT_SECRET", "insecure-dev-secret")
JWT_ALGORITHM = "HS256"
TOKEN_TTL_HOURS = 12

ADMIN_EMAIL = (os.getenv("ADMIN_EMAIL") or "").strip().lower()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or ""


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def random_password(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_token(subject: str, role: str, name: str | None = None) -> str:
    payload = {
        "sub": subject,
        "role": role,
        "name": name or subject,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


def check_admin(email: str, password: str) -> bool:
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        return False
    email_ok = hmac.compare_digest((email or "").strip().lower(), ADMIN_EMAIL)
    pass_ok = hmac.compare_digest(password or "", ADMIN_PASSWORD)
    return email_ok and pass_ok
