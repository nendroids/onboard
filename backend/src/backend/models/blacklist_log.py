# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: blacklist_log                                                                            │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from datetime import datetime, timezone


class BlacklistLog(db.Model):

    __tablename__ = "blacklist_logs"

    id = db.Column(db.Integer, primary_key=True)

    admin_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    target_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    reason = db.Column(db.Text, nullable=False)
    action = db.Column(db.String(20), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    admin = db.relationship(
        "User", foreign_keys=[admin_id], backref="blacklist_actions"
    )

    target = db.relationship(
        "User", foreign_keys=[target_user_id], backref="blacklist_entries"
    )

    def __repr__(self) -> str:
        return f"<BlacklistLog {self.action} target={self.target_user_id}>"
