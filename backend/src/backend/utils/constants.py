# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: constants                                                                                 │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

USER_ROLES = ("admin", "company", "student")

USER_STATUSES = ("pending", "approved", "rejected", "blacklisted")

JOB_STATUSES = ("pending", "approved", "rejected", "closed")

APPLICATION_STATUSES = ("applied", "shortlisted", "interview", "selected", "rejected")

PLACEMENT_STATUSES = ("not_placed", "placed")

ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}
ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "svg", "webp"}

MAX_RESUME_SIZE_MB = 5
MAX_LOGO_SIZE_MB = 2

# Cache TTLs (seconds)
CACHE_TTL_SHORT = 60
CACHE_TTL_MEDIUM = 300
CACHE_TTL_LONG = 900