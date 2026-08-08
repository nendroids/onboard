# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: export                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from datetime import datetime, timezone


class ExportJob(db.Model):

    __tablename__ = "exports"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status = db.Column(db.String(20), default="pending", nullable=False, index=True)

    file_path = db.Column(db.String(512), nullable=True)
    celery_task_id = db.Column(db.String(100), nullable=True)
    error_message = db.Column(db.Text, nullable=True)

    requested_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    student = db.relationship("Student", back_populates="export")

    def __repr__(self) -> str:
        return f"<Exports {self.id} student={self.student_id} status={self.status}>"
