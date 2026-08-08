# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ config: ProductionConfig                                                                         │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations


from backend.config.config import Config


class ProductionConfig(Config):
    DEBUG = False
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_SECURE = True
