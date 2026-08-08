# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: interview                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from backend.models import Interview, Application, Job

VALID_STATUSES = {"scheduled", "completed", "cancelled", "rescheduled"}


class InterviewService:

    @staticmethod
    def update_interview(interview_id, company_id, data):
        interview = (
            Interview.query.join(Application)
            .join(Job, Application.job_id == Job.id)
            .filter(Interview.id == interview_id, Job.company_id == company_id)
            .first()
        )
        if not interview:
            raise ValueError("Interview not found")

        if "status" in data and data["status"] not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {data['status']}")

        for field in ("status", "feedback", "scheduled_at", "mode", "link", "location"):
            if field in data:
                setattr(interview, field, data[field])

        db.session.commit()
        return interview
