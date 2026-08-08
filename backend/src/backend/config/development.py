# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ config: DevelopmentConfig                                                                        │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from .config import Config


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
