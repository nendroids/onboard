# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: helpers                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from flask import request
from werkzeug.utils import secure_filename


def paginate_query(query, page: int = 1, per_page: int = 20, max_per_page: int = 100):
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    return query.paginate(page=page, per_page=per_page, error_out=False)


def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    ext = (
        original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else ""
    )
    unique = uuid.uuid4().hex[:12]
    name = secure_filename(original_filename.rsplit(".", 1)[0])[:40]
    if prefix:
        return f"{prefix}_{name}_{unique}.{ext}" if ext else f"{prefix}_{name}_{unique}"
    return f"{name}_{unique}.{ext}" if ext else f"{name}_{unique}"


def get_client_ip() -> str | None:
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr


def format_datetime(dt: datetime | None, fmt: str = "%Y-%m-%d %H:%M") -> str | None:
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime(fmt)


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except TypeError, ValueError:
        return default


def safe_float(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except TypeError, ValueError:
        return default


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path
