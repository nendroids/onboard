# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: notification                                                                             │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯


from backend.extensions import db
from datetime import datetime, timezone


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False, default="info", index=True)
    link = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    user = db.relationship("User", back_populates="notifications")

    @classmethod
    def create(
        cls,
        user_id: int,
        title: str,
        message: str,
        notif_type: str = "info",
        link: str | None = None,
    ) -> "Notification":
        return cls(
            user_id=user_id,
            title=title,
            message=message,
            type=notif_type,
            link=link,
        )

    def mark_read(self) -> None:
        self.is_read = True

    @property
    def icon_class(self) -> str:
        return {
            "application_update": "bi-person-check",
            "job_approved": "bi-briefcase-fill",
            "job_rejected": "bi-x-circle-fill",
            "company_approved": "bi-building-check",
            "company_rejected": "bi-building-slash",
            "new_application": "bi-envelope-fill",
            "interview": "bi-calendar-event",
            "info": "bi-info-circle-fill",
        }.get(self.type, "bi-bell-fill")

    def __repr__(self) -> str:
        return f"<Notification user={self.user_id} type={self.type!r}>"
