# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: user                                                                                     │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from .base import TimestampMixin
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, TimestampMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)
    status = db.Column(db.String(20), default="pending", nullable=False, index=True)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    blacklist_reason = db.Column(db.Text, nullable=True)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    company_profile = db.relationship(
        "Company",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )

    student_profile = db.relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="user",
        lazy="dynamic",
        foreign_keys="AuditLog.user_id",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self) -> bool:
        if self.is_blacklisted:
            return False
        if self.role == "admin":
            return True
        return self.status == "approved"

    @property
    def unread_notification_count(self) -> int:
        return self.notifications.filter_by(is_read=False).count()

    def record_login(self) -> None:
        self.last_login = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<User {self.username!r} role={self.role!r} status={self.status!r}>"
