# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: security                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

import hashlib
import os
import secrets
from pathlib import Path


def generate_secure_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def hash_file(filepath: str, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_safe_path(basedir: str, path: str) -> bool:
    basedir = os.path.abspath(basedir)
    path = os.path.abspath(os.path.join(basedir, path))
    return path.startswith(basedir)
