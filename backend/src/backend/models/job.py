# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: job                                                                                      │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

import re

from backend.extensions import db
from .base import BaseModel
from datetime import datetime, timezone


class Job(BaseModel):

    __tablename__ = "jobs"

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(500), nullable=True)
    eligibility_criteria = db.Column(db.Text, nullable=True)
    min_cgpa = db.Column(db.Float, nullable=True)
    eligible_branches = db.Column(db.String(300), nullable=True)
    eligible_year = db.Column(db.Integer, nullable=True)
    experience_required = db.Column(db.String(100), nullable=True)
    employment_type = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    openings = db.Column(db.Integer, default=1)
    salary_range = db.Column(db.String(100), nullable=True)
    package_lpa = db.Column(db.Float, nullable=True)
    bond_period = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default="pending", nullable=False, index=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    approved_at = db.Column(db.DateTime(timezone=True), nullable=True)
    deadline = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    company = db.relationship("Company", back_populates="jobs")

    applications = db.relationship(
        "Application",
        back_populates="job",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    placements = db.relationship(
        "Placement",
        back_populates="job",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @staticmethod
    def _coerce_datetime(value):
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @property
    def is_open(self) -> bool:
        if self.status != "approved" or self.deleted_at is not None:
            return False
        deadline = self._coerce_datetime(self.deadline)
        if deadline and datetime.now(timezone.utc) > deadline:
            return False
        return True

    @property
    def is_deadline_passed(self) -> bool:
        deadline = self._coerce_datetime(self.deadline)
        return bool(deadline and datetime.now(timezone.utc) > deadline)

    @property
    def applicant_count(self) -> int:
        return self.applications.filter_by(deleted_at=None).count()

    @property
    def shortlisted_count(self) -> int:
        return self.applications.filter_by(status="shortlisted").count()

    @property
    def selected_count(self) -> int:
        return self.applications.filter_by(status="selected").count()

    @property
    def skills_list(self) -> list[str]:
        if not self.skills_required:
            return []
        return [s.strip() for s in self.skills_required.split(",") if s.strip()]

    @property
    def summary_text(self) -> str:
        desc = (self.description or "").strip()
        if not desc:
            return ""
        # simple extraction of first meaningful paragraph
        cleaned = re.sub(r"^\s*[-*]\s+", "", desc, flags=re.MULTILINE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned[:300] + ("..." if len(cleaned) > 300 else "")

    def approve(self) -> None:
        self.status = "approved"
        self.approved_at = datetime.now(timezone.utc)
        self.rejection_reason = None

    def reject(self, reason: str = "") -> None:
        self.status = "rejected"
        self.rejection_reason = reason

    def close(self) -> None:
        self.status = "closed"

    def __repr__(self) -> str:
        return f"<Job {self.title!r} status={self.status!r}>"
