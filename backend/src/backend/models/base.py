# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: base                                                                                     │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from datetime import datetime, timezone


class TimestampMixin:

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SoftDeleteMixin:

    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(timezone.utc)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class BaseModel(TimestampMixin, SoftDeleteMixin, db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
