# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: placement                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from .base import BaseModel
from datetime import datetime, timezone


class Placement(BaseModel):

    __tablename__ = "placements"

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    offered_salary = db.Column(db.String(100), nullable=True)
    ctc_offered = db.Column(db.String(100), nullable=True)
    offer_letter_path = db.Column(db.String(255), nullable=True)
    joining_date = db.Column(db.DateTime(timezone=True), nullable=True)

    placed_on = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    job = db.relationship("Job", back_populates="placements")
    student = db.relationship("Student", back_populates="placements")

    __table_args__ = (
        db.UniqueConstraint("student_id", "job_id", name="uq_placement_student_job"),
    )

    @property
    def company(self):
        return self.job.company if self.job else None

    def __repr__(self) -> str:
        return f"<Placement student={self.student_id} job={self.job_id}>"
