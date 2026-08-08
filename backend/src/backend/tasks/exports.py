# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ tasks: exports                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

import csv
import os
import logging

from datetime import datetime, timezone, timedelta
from backend.models import Application, Student, Company, Job
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="app.tasks.exports.export_student_applications_task")
def export_student_applications_task(student_id):
    profile = Student.query.get(student_id)
    if not profile:
        return "Student not found"
    os.makedirs("exports", exist_ok=True)
    filename = f'student_{student_id}_apps_{datetime.now().strftime("%Y%m%d")}.csv'
    filepath = os.path.join("exports", filename)
    apps = profile.applications.all()
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Student ID",
                "Full Name",
                "Job Title",
                "Company",
                "Status",
                "Applied On",
                "Updated At",
            ]
        )
        for a in apps:
            writer.writerow(
                [
                    profile.student_id,
                    profile.full_name,
                    a.job.title if a.job else "",
                    a.job.company.name if a.job and a.job.company else "",
                    a.status,
                    a.applied_on.isoformat() if a.applied_on else "",
                    a.updated_at.isoformat() if a.updated_at else "",
                ]
            )
    return filepath


@shared_task(name="app.tasks.exports.export_company_applications_task")
def export_company_applications_task(company_id):
    company = Company.query.get(company_id)
    if not company:
        return "Company not found"
    os.makedirs("exports", exist_ok=True)
    filename = f'company_{company_id}_apps_{datetime.now().strftime("%Y%m%d")}.csv'
    filepath = os.path.join("exports", filename)
    apps = Application.query.join(Job).filter(Job.company_id == company_id).all()
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Application ID",
                "Student Name",
                "Student ID",
                "Job Title",
                "Status",
                "Applied On",
                "Feedback",
            ]
        )
        for a in apps:
            student = a.student
            writer.writerow(
                [
                    a.id,
                    student.full_name if student else "",
                    student.student_id if student else "",
                    a.job.title if a.job else "",
                    a.status,
                    a.applied_on.isoformat() if a.applied_on else "",
                    a.feedback or "",
                ]
            )
    return filepath


@shared_task(name="app.tasks.utils.export_cleanup_task")
def export_cleanup_task(days: int = 30) -> str:
    export_dir = "exports"  # matches the directory used in exports.py
    if not os.path.isdir(export_dir):
        return f"Export directory '{export_dir}' does not exist."

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    deleted = 0

    for filename in os.listdir(export_dir):
        filepath = os.path.join(export_dir, filename)
        if not os.path.isfile(filepath) or not filename.endswith(".csv"):
            continue

        mtime = datetime.fromtimestamp(os.path.getmtime(filepath), tz=timezone.utc)
        if mtime < cutoff:
            try:
                os.remove(filepath)
                deleted += 1
                logger.info("Deleted old export file: %s", filename)
            except OSError as e:
                logger.error("Failed to delete %s: %s", filename, e)

    return f"Deleted {deleted} export file(s) older than {days} days."
