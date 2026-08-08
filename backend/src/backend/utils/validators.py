# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: validators                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

import re
from urllib.parse import urlparse

from .constants import ALLOWED_RESUME_EXTENSIONS, ALLOWED_LOGO_EXTENSIONS
from .exceptions import ValidationError

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PHONE_REGEX = re.compile(r"^\+?[\d\s\-()]{7,20}$")


def validate_email(email: str) -> str:
    email = (email or "").strip().lower()
    if not email or not EMAIL_REGEX.match(email):
        raise ValidationError("Invalid email address")
    return email


def validate_password(password: str, min_length: int = 8) -> str:
    if not password or len(password) < min_length:
        raise ValidationError(f"Password must be at least {min_length} characters")
    return password


def validate_cgpa(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        cgpa = float(value)
    except TypeError, ValueError:
        raise ValidationError("CGPA must be a number")
    if not (0.0 <= cgpa <= 10.0):
        raise ValidationError("CGPA must be between 0.0 and 10.0")
    return cgpa


def validate_phone(phone: str | None) -> str | None:
    if not phone:
        return None
    phone = phone.strip()
    if not PHONE_REGEX.match(phone):
        raise ValidationError("Invalid phone number")
    return phone


def validate_url(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip()
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValidationError("Invalid URL")
    return url


def sanitize_string(value: str | None, max_length: int | None = None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.strip().split())
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned or None


def validate_file_extension(filename: str, allowed: set[str]) -> str:
    if "." not in filename:
        raise ValidationError("File has no extension")
    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in allowed:
        raise ValidationError(f"Allowed extensions: {', '.join(sorted(allowed))}")
    return ext


def validate_resume_filename(filename: str) -> str:
    return validate_file_extension(filename, ALLOWED_RESUME_EXTENSIONS)


def validate_logo_filename(filename: str) -> str:
    return validate_file_extension(filename, ALLOWED_LOGO_EXTENSIONS)
