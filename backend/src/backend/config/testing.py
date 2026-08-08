# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ config: TestingConfig                                                                            │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from .config import Config


class TestingConfig(Config):
    CACHE_TYPE = "SimpleCache"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
