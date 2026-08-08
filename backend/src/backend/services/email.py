# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: email                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from flask import current_app
from flask_mail import Message
from backend.extensions import mail


class EmailService:
    @staticmethod
    def send_email(
        to: str | list[str], subject: str, html_body: str, text_body: str | None = None
    ):
        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to,
            html=html_body,
            body=text_body or "",
        )
        mail.send(msg)

    @staticmethod
    def send_deadline_reminder(student_email: str, job_title: str, deadline: str):
        html = f"""
        <h3>Application Deadline Reminder</h3>
        <p>The application deadline for <strong>{job_title}</strong> is approaching: {deadline}.</p>
        <p>Please submit your application before the deadline.</p>
        """
        EmailService.send_email(
            to=student_email,
            subject=f"Reminder: Deadline for {job_title}",
            html_body=html,
        )
