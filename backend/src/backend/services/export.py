# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: export                                                                                 │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from backend.extensions import db, celery
from backend.models import ExportJob, Application, Job, Company


@celery.task(bind=True)
def generate_applications_csv(self, export_job_id: int):
    """Celery task – generate CSV of student's applications."""
    export_job = ExportJob.query.get(export_job_id)
    if not export_job:
        return

    try:
        export_job.status = "processing"
        export_job.celery_task_id = self.request.id
        db.session.commit()

        apps = (
            Application.query.filter_by(student_id=export_job.student_id)
            .filter(Application.deleted_at.is_(None))
            .join(Job)
            .join(Company)
            .add_columns(
                Application.id,
                Application.status,
                Application.applied_on,
                Job.title,
                Company.name,
            )
            .all()
        )

        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        filename = f"applications_student_{export_job.student_id}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = export_dir / filename

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Application ID", "Company Name", "Job Title", "Status", "Applied On"]
            )
            for row in apps:
                writer.writerow(
                    [
                        row.id,
                        row.name,
                        row.title,
                        row.status,
                        row.applied_on.isoformat() if row.applied_on else "",
                    ]
                )

        export_job.status = "completed"
        export_job.file_path = str(filepath)
        export_job.completed_at = datetime.now(timezone.utc)
        db.session.commit()

        # Optional: send notification that export is ready
        from backend.models import Notification

        Notification.create(
            user_id=export_job.student.user_id,
            title="Export Ready",
            message="Your application history CSV is ready for download.",
            notif_type="info",
            link=f"/student/exports/{export_job.id}",
        )
        db.session.commit()

    except Exception as exc:
        export_job.status = "failed"
        export_job.error_message = str(exc)
        db.session.commit()
        raise


class ExportService:
    @staticmethod
    def request_export(student_id: int) -> ExportJob:
        export_job = ExportJob(student_id=student_id, status="pending")
        db.session.add(export_job)
        db.session.commit()

        # Fire async task
        generate_applications_csv.delay(export_job.id)
        return export_job
