# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: students                                                                               │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from backend.extensions import db, cache
from backend.models import Student, Job, Application, Placement, Notification
from backend.services.eligibility import EligibilityService


class StudentService:

    @staticmethod
    def get_dashboard(student_id: int) -> dict[str, Any]:
        student = Student.query.get_or_404(student_id)
        open_jobs = (
            Job.query.filter_by(status="approved")
            .filter(Job.deleted_at.is_(None))
            .order_by(Job.deadline.asc().nullslast())
            .limit(20)
            .all()
        )
        my_apps = (
            Application.query.filter_by(student_id=student_id)
            .filter(Application.deleted_at.is_(None))
            .options(joinedload(Application.job).joinedload(Job.company))
            .order_by(Application.applied_on.desc())
            .limit(10)
            .all()
        )
        return {
            "student": student,
            "open_jobs": open_jobs,
            "recent_applications": my_apps,
            "active_count": student.active_applications_count,
            "is_placed": student.is_placed,
        }

    @staticmethod
    def update_profile(student_id: int, data: dict[str, Any]) -> Student:
        student = Student.query.get_or_404(student_id)
        allowed = {
            "full_name",
            "phone",
            "education",
            "branch",
            "cgpa",
            "graduation_year",
            "skills",
            "certifications",
            "headline",
            "about_me",
            "experience",
            "preferred_roles",
            "github_url",
            "linkedin_url",
            "portfolio_url",
        }
        for key, value in data.items():
            if key in allowed:
                setattr(student, key, value)
        db.session.commit()
        return student

    @staticmethod
    def search_jobs(
        student_id: int,
        q: str | None = None,
        skills: str | None = None,
        page: int = 1,
        per_page: int = 12,
    ):
        student = Student.query.get_or_404(student_id)
        query = (
            Job.query.filter_by(status="approved")
            .filter(Job.deleted_at.is_(None))
            .options(joinedload(Job.company))
        )
        if q:
            query = query.filter(
                or_(
                    Job.title.ilike(f"%{q}%"),
                    Job.description.ilike(f"%{q}%"),
                    Job.location.ilike(f"%{q}%"),
                )
            )
        if skills:
            for skill in skills.split(","):
                skill = skill.strip()
                if skill:
                    query = query.filter(Job.skills_required.ilike(f"%{skill}%"))

        # Optional: filter by eligibility
        jobs = query.order_by(Job.deadline.asc().nullslast()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return jobs

    @staticmethod
    def apply_to_job(
        student_id: int,
        job_id: int,
        cover_letter: str | None = None,
    ) -> Application:
        student = Student.query.get_or_404(student_id)
        job = Job.query.filter_by(id=job_id, status="approved").first_or_404()

        if not job.is_open:
            raise ValueError("This job is no longer open for applications")

        # Prevent duplicate
        existing = (
            Application.query.filter_by(student_id=student_id, job_id=job_id)
            .filter(Application.deleted_at.is_(None))
            .first()
        )
        if existing:
            raise ValueError("You have already applied to this job")

        EligibilityService.check(student, job)

        application = Application(
            student_id=student_id,
            job_id=job_id,
            cover_letter=cover_letter,
            status="applied",
        )
        db.session.add(application)
        db.session.commit()

        # Notify company
        Notification.create(
            user_id=job.company.user_id,
            title="New Application Received",
            message=f"{student.full_name} applied for '{job.title}'.",
            notif_type="new_application",
            link=f"/company/jobs/{job.id}/applicants",
        )
        db.session.commit()
        return application

    @staticmethod
    def get_my_applications(student_id: int):
        return (
            Application.query.filter_by(student_id=student_id)
            .filter(Application.deleted_at.is_(None))
            .options(
                joinedload(Application.job).joinedload(Job.company),
                joinedload(Application.interview),
            )
            .order_by(Application.applied_on.desc())
            .all()
        )

    @staticmethod
    def get_placement_history(student_id: int):
        return (
            Placement.query.filter_by(student_id=student_id)
            .options(joinedload(Placement.job).joinedload(Job.company))
            .order_by(Placement.placed_on.desc())
            .all()
        )
