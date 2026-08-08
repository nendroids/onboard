# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: health                                                                                       │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import jsonify
from sqlalchemy import text

from . import api_v1
from backend.extensions import db, cache


@api_v1.get("/health")
def health_check():
    status = {"status": "ok", "database": "ok", "cache": "ok"}

    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        status["database"] = "error"
        status["status"] = "degraded"

    try:
        cache.set("health_check", "ok", timeout=5)
        if cache.get("health_check") != "ok":
            raise RuntimeError("Cache failed")
    except Exception:
        status["cache"] = "error"
        status["status"] = "degraded"

    return jsonify(status), 200 if status["status"] == "ok" else 503
