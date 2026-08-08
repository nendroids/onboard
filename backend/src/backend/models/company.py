# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: company                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from .base import BaseModel
from datetime import datetime, timezone


class Company(BaseModel):

    __tablename__ = "companies"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    name = db.Column(db.String(150), nullable=False, index=True)
    industry = db.Column(db.String(100), nullable=True, index=True)
    website = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    company_size = db.Column(db.String(50), nullable=True)
    established_year = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(150), nullable=True)
    logo_path = db.Column(db.String(255), nullable=True)
    hr_name = db.Column(db.String(150), nullable=True)
    hr_email = db.Column(db.String(120), nullable=True)
    hr_phone = db.Column(db.String(20), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    approved_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)

    user = db.relationship("User", back_populates="company_profile")
    jobs = db.relationship(
        "Job",
        back_populates="company",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @property
    def is_approved(self) -> bool:
        return self.approved_at is not None and self.deleted_at is None

    @property
    def active_jobs_count(self) -> int:
        return self.jobs.filter_by(status="approved").count()

    @property
    def total_applicants(self) -> int:
        from .application import Application
        from .job import Job

        return (
            Application.query.join(Job)
            .filter(Job.company_id == self.id, Application.deleted_at.is_(None))
            .count()
        )

    def approve(self) -> None:
        self.approved_at = datetime.now(timezone.utc)
        self.rejection_reason = None
        if self.user:
            self.user.status = "approved"

    def reject(self, reason: str = "") -> None:
        self.approved_at = None
        self.rejection_reason = reason
        if self.user:
            self.user.status = "rejected"

    def __repr__(self) -> str:
        return f"<Company {self.name!r}>"
