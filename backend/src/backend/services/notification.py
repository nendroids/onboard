# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: notification                                                                           │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from backend.extensions import db
from backend.models import Notification


class NotificationService:
    @staticmethod
    def get_user_notifications(
        user_id: int, unread_only: bool = False, limit: int = 50
    ):
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> Notification:
        notif = Notification.query.filter_by(
            id=notification_id, user_id=user_id
        ).first_or_404()
        notif.mark_read()
        db.session.commit()
        return notif

    @staticmethod
    def mark_all_read(user_id: int) -> int:
        count = Notification.query.filter_by(user_id=user_id, is_read=False).update(
            {"is_read": True}
        )
        db.session.commit()
        return count
