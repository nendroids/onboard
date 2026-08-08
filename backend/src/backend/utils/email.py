# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: email                                                                                     │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import current_app
from flask_mail import Message

from backend.extensions import mail


def send_email(
    to: str | list[str],
    subject: str,
    body: str,
    html: str | None = None,
) -> bool:
    """
    Send an email.
    Returns True on success, False on failure.
    Never raises – logs errors instead.
    """
    recipients = [to] if isinstance(to, str) else to
    msg = Message(subject=subject, recipients=recipients, body=body)
    if html:
        msg.html = html

    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Email send failed to {recipients}: {e}")
        return False
