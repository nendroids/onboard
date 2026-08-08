# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: audit_log                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from datetime import datetime, timezone


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True, index=True
    )

    action = db.Column(db.String(100), nullable=False, index=True)
    entity_type = db.Column(db.String(50), nullable=True)
    entity_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    performed_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False,
    )

    user = db.relationship("User", back_populates="audit_logs", foreign_keys=[user_id])

    @classmethod
    def log(
        cls,
        action: str,
        user_id: int | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
        details: str | None = None,
        ip_address: str | None = None,
    ) -> "AuditLog":
        return cls(
            action=action,
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
        )

    def __repr__(self) -> str:
        return f"<AuditLog {self.action!r} user={self.user_id}>"
