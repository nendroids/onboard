# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ config: Config                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

import os

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

from backend.utils.dirs import (
    dir_backend,
    dir_backups,
    dir_company_docs,
    dir_exports,
    dir_instance,
    dir_logos,
    dir_offer_letters,
    dir_private,
    dir_public,
    dir_reports,
    dir_resumes,
    dir_storage,
    dir_student_docs,
    dir_temporary,
)


class Config:
    # SECURITY
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    # FOLDERS
    BACKEND_FOLDER = dir_backend
    INSTANCE_FOLDER = dir_instance
    STORAGE_FOLDER = dir_storage
    PUBLIC_FOLDER = dir_public
    PRIVATE_FOLDER = dir_private
    EXPORTS_FOLDER = dir_exports
    REPORTS_FOLDER = dir_reports
    TEMP_FOLDER = dir_temporary
    BACKUP_FOLDER = dir_backups
    RESUME_FOLDER = dir_resumes
    LOGO_FOLDER = dir_logos
    OFFER_LETTER_FOLDER = dir_offer_letters
    COMPANY_DOCS_FOLDER = dir_company_docs
    STUDENT_DOCS_FOLDER = dir_student_docs

    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{INSTANCE_FOLDER.joinpath('onboard.sqlite3').resolve().as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # JSON
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    # REDIS
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_URL = os.getenv("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

    # CACHE
    CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")
    CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.getenv("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_URL = os.getenv(
        "CACHE_REDIS_URL", f"redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/0"
    )
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))

    # CELERY
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "Asia/Kolkata")

    # MAIL
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "1", "t", "yes"]
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ["true", "1", "t", "yes"]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER", "noreply.iic@study.iitm.ac.in"
    )

    # GOOGLE CHAT WEBHOOK
    GCHAT_WEBHOOK_URL = os.getenv("GCHAT_WEBHOOK_URL", "")

    # SESSION
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # STORAGE
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    # EXTENSIONS
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}
    ALLOWED_EXPORT_EXTENSIONS = {"csv", "xlsx", "pdf"}
    ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "svg"}

    # PAGINATION
    PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    # URLS
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
