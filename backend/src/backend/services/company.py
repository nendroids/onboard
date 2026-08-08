# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: company                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import joinedload

from backend.extensions import db, cache
from backend.models import (
    Company,
    Job,
    Application,
    Interview,
    Notification,
    AuditLog,
    Placement,
    Student,
)


class CompanyService:

    @staticmethod
    def get_dashboard(company_id: int) -> dict[str, Any]:
        company = (
            Company.query.options(joinedload(Company.user))
            .filter_by(id=company_id, deleted_at=None)
            .first_or_404()
        )
        if not company.is_approved:
            raise ValueError("Company not yet approved")

        jobs = (
            Job.query.filter_by(company_id=company_id)
            .filter(Job.deleted_at.is_(None))
            .order_by(Job.created_at.desc())
            .all()
        )

        return {
            "company": company,
            "jobs": jobs,
            "stats": {
                "total_jobs": len(jobs),
                "active_jobs": sum(1 for j in jobs if j.is_open),
                "total_applicants": company.total_applicants,
            },
        }

    @staticmethod
    def create_job(company_id: int, data: dict[str, Any]) -> Job:
        company = Company.query.get_or_404(company_id)
        if not company.is_approved:
            raise ValueError("Only approved companies can post jobs")

        job = Job(
            company_id=company_id,
            title=data["title"],
            description=data["description"],
            skills_required=data.get("skills_required"),
            eligibility_criteria=data.get("eligibility_criteria"),
            min_cgpa=data.get("min_cgpa"),
            eligible_branches=data.get("eligible_branches"),
            eligible_year=data.get("eligible_year"),
            experience_required=data.get("experience_required"),
            employment_type=data.get("employment_type"),
            location=data.get("location"),
            openings=data.get("openings", 1),
            salary_range=data.get("salary_range"),
            package_lpa=data.get("package_lpa"),
            bond_period=data.get("bond_period"),
            deadline=data.get("deadline"),
            status="pending",
        )
        db.session.add(job)
        db.session.commit()

        AuditLog.log(
            action="job_created",
            user_id=company.user_id,
            entity_type="job",
            entity_id=job.id,
        )
        db.session.commit()
        cache.delete("admin_dashboard_stats")
        return job

    @staticmethod
    def update_job(job_id: int, company_id: int, data: dict[str, Any]) -> Job:
        job = Job.query.filter_by(id=job_id, company_id=company_id).first_or_404()
        if job.status not in ("pending", "approved"):
            raise ValueError("Cannot edit a closed/rejected job")

        for field in (
            "title",
            "description",
            "skills_required",
            "eligibility_criteria",
            "min_cgpa",
            "eligible_branches",
            "eligible_year",
            "experience_required",
            "employment_type",
            "location",
            "openings",
            "salary_range",
            "package_lpa",
            "bond_period",
            "deadline",
        ):
            if field in data:
                setattr(job, field, data[field])

        if job.status == "approved":
            job.status = "pending"
            job.approved_at = None

        db.session.commit()
        return job

    @staticmethod
    def get_applicants(job_id: int, company_id: int, status: str | None = None):
        job = Job.query.filter_by(id=job_id, company_id=company_id).first_or_404()
        query = (
            Application.query.options(
                joinedload(Application.student).joinedload(Student.user),
                joinedload(Application.interview),
            )
            .filter_by(job_id=job.id)
            .filter(Application.deleted_at.is_(None))
        )
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Application.applied_on.desc()).all()

    @staticmethod
    def update_application_status(
        application_id: int,
        company_id: int,
        new_status: str,
        feedback: str | None = None,
    ) -> Application:
        app = Application.query.options(
            joinedload(Application.job),
            joinedload(Application.student).joinedload(Student.user),
        ).get_or_404(application_id)
        if app.job.company_id != company_id:
            raise PermissionError("Not your job")

        app.update_status(new_status, feedback=feedback)
        db.session.commit()

        Notification.create(
            user_id=app.student.user_id,
            title="Application Status Updated",
            message=f"Your application for '{app.job.title}' is now {new_status}.",
            notif_type="application_update",
            link=f"/student/applications/{app.id}",
        )
        db.session.commit()
        return app

    @staticmethod
    def schedule_interview(
        application_id: int,
        company_id: int,
        scheduled_at: datetime,
        mode: str | None = None,
        link: str | None = None,
        location: str | None = None,
    ) -> Interview:
        app = Application.query.options(joinedload(Application.job)).get_or_404(
            application_id
        )
        if app.job.company_id != company_id:
            raise PermissionError("Not your job")

        if app.status not in ("shortlisted", "interview"):
            raise ValueError("Can only schedule interview for shortlisted candidates")

        if app.interview:
            interview = app.interview
            interview.scheduled_at = scheduled_at
            interview.mode = mode
            interview.link = link
            interview.location = location
            interview.status = "scheduled"
        else:
            interview = Interview(
                application_id=application_id,
                scheduled_at=scheduled_at,
                mode=mode,
                link=link,
                location=location,
            )
            db.session.add(interview)

        app.status = "interview"
        db.session.commit()

        Notification.create(
            user_id=app.student.user_id,
            title="Interview Scheduled",
            message=f"Interview for '{app.job.title}' scheduled on {scheduled_at}.",
            notif_type="interview",
            link=f"/student/applications/{app.id}",
        )
        db.session.commit()
        return interview

    @staticmethod
    def select_candidate(
        application_id: int,
        company_id: int,
        offered_salary: str | None = None,
        ctc_offered: str | None = None,
        joining_date: datetime | None = None,
    ) -> Placement:
        app = Application.query.options(
            joinedload(Application.job),
            joinedload(Application.student),
        ).get_or_404(application_id)
        if app.job.company_id != company_id:
            raise PermissionError("Not your job")

        app.update_status("selected")
        app.student.mark_placed()

        placement = Placement(
            job_id=app.job_id,
            student_id=app.student_id,
            offered_salary=offered_salary,
            ctc_offered=ctc_offered,
            joining_date=joining_date,
        )
        db.session.add(placement)
        db.session.commit()

        Notification.create(
            user_id=app.student.user_id,
            title="Congratulations! You are Selected",
            message=f"You have been selected for '{app.job.title}'.",
            notif_type="application_update",
        )
        db.session.commit()
        return placement
