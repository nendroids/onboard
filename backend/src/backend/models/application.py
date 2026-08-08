# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: application                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from .base import BaseModel
from datetime import datetime, timezone


class Application(BaseModel):

    __tablename__ = "applications"

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status = db.Column(db.String(20), default="applied", nullable=False, index=True)

    cover_letter = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    applied_on = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    student = db.relationship("Student", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")

    interview = db.relationship(
        "Interview",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        db.UniqueConstraint("student_id", "job_id", name="uq_student_job"),
        db.Index("ix_app_status_job", "status", "job_id"),
    )

    STATUSES = ("applied", "shortlisted", "interview", "selected", "rejected")

    def update_status(self, new_status: str, feedback: str | None = None) -> None:
        if new_status not in self.STATUSES:
            raise ValueError(f"Invalid status: {new_status!r}")
        self.status = new_status
        if feedback is not None:
            self.feedback = feedback

    @property
    def is_active(self) -> bool:
        return self.status not in ("selected", "rejected") and self.deleted_at is None

    @property
    def badge_class(self) -> str:
        return {
            "applied": "bg-secondary",
            "shortlisted": "bg-info",
            "interview": "bg-warning text-dark",
            "selected": "bg-success",
            "rejected": "bg-danger",
        }.get(self.status, "bg-secondary")

    def __repr__(self) -> str:
        return f"<Application student={self.student_id} job={self.job_id} status={self.status!r}>"
