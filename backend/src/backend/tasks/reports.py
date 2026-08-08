# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ tasks: reports                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from backend.extensions import db
from backend.models import Job, Application, Placement, User
from backend.utils.email import send_email
from celery import shared_task


@shared_task(name="app.tasks.reports.generate_monthly_admin_report")
def generate_monthly_admin_report():
    now = datetime.now()
    first_day_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = now.replace(day=1) - timedelta(days=1)

    jobs = Job.query.filter(
        Job.created_at >= first_day_last_month, Job.created_at <= last_day_last_month
    ).count()
    apps = Application.query.filter(
        Application.applied_on >= first_day_last_month,
        Application.applied_on <= last_day_last_month,
    ).count()
    selected = Application.query.filter(
        Application.status == "selected",
        Application.updated_at >= first_day_last_month,
        Application.updated_at <= last_day_last_month,
    ).count()
    placements = Placement.query.filter(
        Placement.placed_on >= first_day_last_month,
        Placement.placed_on <= last_day_last_month,
    ).count()

    report = [
        f'Monthly Activity Report - {first_day_last_month.strftime("%B %Y")}',
        "-" * 40,
        f"Drives Posted: {jobs}",
        f"Applications: {apps}",
        f"Students Selected: {selected}",
        f"Final Placements: {placements}",
        "-" * 40,
        f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}',
    ]
    admin = User.query.filter_by(role="admin").first()
    if admin:
        send_email(
            admin.email,
            f'Monthly Report - {first_day_last_month.strftime("%B %Y")}',
            "\n".join(report),
        )
    return f'Report sent to {admin.email if admin else "no admin"}.'
