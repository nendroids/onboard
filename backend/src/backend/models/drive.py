# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: drive                                                                                    │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from .base import BaseModel


class PlacementDrive(BaseModel):

    __tablename__ = "placement_drives"

    company_id = db.Column(
        db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True
    )

    job_title = db.Column(db.String(100), nullable=False, index=True)
    job_description = db.Column(db.Text, nullable=False)
    eligible_branches = db.Column(db.String(200), nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    eligible_year = db.Column(db.Integer, nullable=False)
    package_lpa = db.Column(db.Float, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    rejection_reason = db.Column(db.String(300), nullable=True)

    applications = db.relationship(
        "Application", backref="drive", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<PlacementDrive {self.job_title} ({self.status})>"
