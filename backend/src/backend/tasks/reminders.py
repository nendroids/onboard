# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ tasks: remainder                                                                                 │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from backend.extensions import db
from backend.models import Application, Notification, Interview, Job, Student
from backend.utils.email import send_email
from celery import shared_task


@shared_task(name="app.tasks.reminders.send_daily_reminders")
def send_daily_reminders():
    now = datetime.now(timezone.utc)
    two_days_later = now + timedelta(days=2)

    upcoming_jobs = Job.query.filter(
        Job.status == "approved",
        Job.deleted_at.is_(None),
        Job.deadline.isnot(None),
        Job.deadline >= now,
        Job.deadline <= two_days_later,
    ).all()

    if not upcoming_jobs:
        return "No upcoming deadlines."

    students = (
        Student.query.join(Student.user)
        .filter(
            Student.user.has(role="student", status="approved", is_blacklisted=False)
        )
        .all()
    )

    for student in students:
        if not student.user or not student.user.email:
            continue
        subject = "Upcoming Placement Drive Deadlines"
        body = (
            f"Hello {student.full_name},\n\n"
            f"There are {len(upcoming_jobs)} approved placement drives with application deadlines approaching in the next 48 hours."
            "\nPlease log in to your dashboard to view and apply.\n\nBest regards,\nPlacement Portal Team"
        )
        send_email(student.user.email, subject, body)
        notification = Notification(
            user_id=student.user_id,
            title="Upcoming Drive Deadlines",
            message=(
                f"{len(upcoming_jobs)} placement drives close in the next 48 hours. Check approved drives now."
            ),
            type="reminder",
            link="/student/drives",
        )
        db.session.add(notification)
    db.session.commit()
    return f"Sent deadline reminders to {len(students)} students."


@shared_task(name="app.tasks.reminders.send_interview_reminders")
def send_interview_reminders():
    now = datetime.now(timezone.utc)
    two_days_later = now + timedelta(days=2)

    interviews = Interview.query.filter(
        Interview.scheduled_at >= now,
        Interview.scheduled_at <= two_days_later,
        Interview.status == "scheduled",
    ).all()

    for interview in interviews:
        application = interview.application
        student = application.student if application else None
        if not student or not student.user or not student.user.email:
            continue
        job_title = application.job.title if application.job else "your interview"
        subject = "Upcoming Interview Reminder"
        body = (
            f"Hello {student.full_name},\n\n"
            f"Your interview for {job_title} is scheduled on {interview.scheduled_at.isoformat()}. Please be prepared.\n\nRegards,\nPlacement Portal Team"
        )
        send_email(student.user.email, subject, body)
        notification = Notification(
            user_id=student.user_id,
            title="Interview Reminder",
            message=(
                f"Interview for {job_title} scheduled on {interview.scheduled_at.isoformat()}."
            ),
            type="interview",
            link=(
                f"/student/applications/{application.id}"
                if application
                else "/student/applications"
            ),
        )
        db.session.add(notification)
    db.session.commit()
    return f"Sent interview reminders for {len(interviews)} interviews."
    for app in apps:
        student = app.student
        if not student or not student.user:
            continue
        job = app.job
        subject = f"Upcoming Interview: {job.title}"
        body = f'Dear {student.full_name},\n\nYou have an interview for {job.title} at {job.company.name} on {app.interview_date.strftime("%Y-%m-%d %H:%M")}. Good luck!'
        send_email(student.user.email, subject, body)
        notif = Notification.create(
            user_id=student.user.id,
            title="Interview Reminder",
            message=f'Interview for {job.title} on {app.interview_date.strftime("%Y-%m-%d %H:%M")}.',
            notif_type="reminder",
            link="/student/applications",
        )
        db.session.add(notif)
    db.session.commit()
    return f"Sent {len(apps)} reminders."
