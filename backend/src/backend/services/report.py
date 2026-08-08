# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: reports                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from datetime import datetime, timezone
from calendar import monthrange

from sqlalchemy import func

from backend.extensions import db
from backend.models import Job, Application, Placement, Company, Student


class ReportService:

    @staticmethod
    def generate_monthly_stats(year: int, month: int) -> dict:
        start = datetime(year, month, 1, tzinfo=timezone.utc)
        last_day = monthrange(year, month)[1]
        end = datetime(year, month, last_day, 23, 59, 59, tzinfo=timezone.utc)

        drives_conducted = Job.query.filter(
            Job.approved_at >= start,
            Job.approved_at <= end,
            Job.status.in_(["approved", "closed"]),
        ).count()

        applications = Application.query.filter(
            Application.applied_on >= start,
            Application.applied_on <= end,
        ).count()

        selected = Application.query.filter(
            Application.status == "selected",
            Application.updated_at >= start,
            Application.updated_at <= end,
        ).count()

        placements = Placement.query.filter(
            Placement.placed_on >= start,
            Placement.placed_on <= end,
        ).count()

        return {
            "period": f"{year}-{month:02d}",
            "drives_conducted": drives_conducted,
            "applications_received": applications,
            "students_selected": selected,
            "placements_confirmed": placements,
        }
