# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ v1: init                                                                                         ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

from . import (
    admin,
    application,
    auth,
    company,
    drive,
    export,
    health,
    interview,
    placement,
    student,
)

__all__ = [
    "admin",
    "application",
    "auth",
    "company",
    "drive",
    "export",
    "health",
    "interview",
    "placement",
    "student",
]
