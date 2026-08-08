# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: interview                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from .base import TimestampMixin
from datetime import datetime, timezone


class Interview(TimestampMixin, db.Model):

    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    scheduled_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    mode = db.Column(db.String(50), nullable=True)
    link = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="scheduled", nullable=False)
    application = db.relationship("Application", back_populates="interview")

    def __repr__(self) -> str:
        return f"<Interview application={self.application_id} at {self.scheduled_at}>"
