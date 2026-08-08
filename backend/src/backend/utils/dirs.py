# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: dirs                                                                                      │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
INSTANCE_DIR = BACKEND_ROOT.joinpath("instance")


def p(*parts: str) -> Path:
    return INSTANCE_DIR.joinpath(*parts)


dir_backend = BACKEND_ROOT
dir_instance = INSTANCE_DIR
dir_exports = p("exports")
dir_reports = p("reports")
dir_backups = p("backups")
dir_temporary = p("temp")
dir_storage = p("storage")
dir_public = p("storage", "public")
dir_private = p("storage", "private")
dir_uploads = p("uploads")
dir_logos = p("uploads", "logos")
dir_resumes = p("uploads", "resumes")
dir_offer_letters = p("uploads", "offer_letters")
dir_docs = p("uploads", "docs")
dir_company_docs = p("uploads", "docs", "company")
dir_student_docs = p("uploads", "docs", "student")


def ensure_directories(instance_dir: str | Path | None = None) -> Path:
    """
    Create the complete storage tree under instance/:

    instance/
    ├── exports/
    ├── reports/
    ├── backups/
    ├── temp/
    ├── storage/
    │   ├── public/
    │   └── private/
    └── uploads/
        ├── logos/
        ├── resumes/
        ├── offer_letters/
        └── docs/
            ├── company/
            └── student/
    """
    root = Path(instance_dir) if instance_dir else INSTANCE_DIR

    directories = [
        dir_exports,
        dir_reports,
        dir_backups,
        dir_temporary,
        dir_storage,
        dir_public,
        dir_private,
        dir_uploads,
        dir_logos,
        dir_resumes,
        dir_offer_letters,
        dir_docs,
        dir_company_docs,
        dir_student_docs,
    ]

    root.mkdir(parents=True, exist_ok=True)

    for directory in directories:
        root.joinpath(directory.relative_to(INSTANCE_DIR)).mkdir(
            parents=True,
            exist_ok=True,
        )

    return root


dir_exports_str = str(dir_exports)
dir_reports_str = str(dir_reports)
dir_uploads_str = str(dir_uploads)
dir_logos_str = str(dir_logos)
dir_resumes_str = str(dir_resumes)
dir_offer_letters_str = str(dir_offer_letters)
dir_docs_str = str(dir_docs)
dir_company_docs_str = str(dir_company_docs)
dir_student_docs_str = str(dir_student_docs)
dir_storage_str = str(dir_storage)
dir_public_str = str(dir_public)
dir_private_str = str(dir_private)
dir_temporary_str = str(dir_temporary)
dir_backups_str = str(dir_backups)
