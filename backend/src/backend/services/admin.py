# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: admin                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload

from backend.extensions import db, cache
from backend.models import (
    User,
    Student,
    Company,
    Job,
    Application,
    BlacklistLog,
    AuditLog,
    Notification,
)


class AdminService:

    @staticmethod
    @cache.cached(timeout=60, key_prefix="admin_dashboard_stats")
    def get_dashboard_stats() -> dict[str, int]:
        return {
            "total_students": Student.query.filter(
                Student.deleted_at.is_(None)
            ).count(),
            "total_companies": Company.query.filter(
                Company.deleted_at.is_(None)
            ).count(),
            "total_jobs": Job.query.filter(Job.deleted_at.is_(None)).count(),
            "total_applications": Application.query.filter(
                Application.deleted_at.is_(None)
            ).count(),
            "pending_companies": Company.query.filter(
                Company.approved_at.is_(None), Company.deleted_at.is_(None)
            ).count(),
            "pending_jobs": Job.query.filter_by(status="pending").count(),
            "placed_students": Student.query.filter_by(
                placement_status="placed"
            ).count(),
        }

    @staticmethod
    def approve_company(company_id: int, admin_id: int) -> Company:
        company = Company.query.options(joinedload(Company.user)).get_or_404(company_id)
        if company.is_approved:
            raise ValueError("Company already approved")

        company.approve()
        db.session.commit()

        Notification.create(
            user_id=company.user_id,
            title="Company Approved",
            message=f"Your company '{company.name}' has been approved.",
            notif_type="company_approved",
        )
        AuditLog.log(
            action="company_approved",
            user_id=admin_id,
            entity_type="company",
            entity_id=company.id,
        )
        db.session.commit()
        cache.delete("admin_dashboard_stats")
        return company

    @staticmethod
    def reject_company(company_id: int, reason: str, admin_id: int) -> Company:
        company = Company.query.options(joinedload(Company.user)).get_or_404(company_id)
        company.reject(reason=reason)
        db.session.commit()

        Notification.create(
            user_id=company.user_id,
            title="Company Rejected",
            message=f"Your company registration was rejected. Reason: {reason}",
            notif_type="company_rejected",
        )
        AuditLog.log(
            action="company_rejected",
            user_id=admin_id,
            entity_type="company",
            entity_id=company.id,
            details=reason,
        )
        db.session.commit()
        cache.delete("admin_dashboard_stats")
        return company

    @staticmethod
    def approve_job(job_id: int, admin_id: int) -> Job:
        job = Job.query.options(joinedload(Job.company)).get_or_404(job_id)
        if job.status != "pending":
            raise ValueError(f"Job is already {job.status}")

        job.approve()
        db.session.commit()

        Notification.create(
            user_id=job.company.user_id,
            title="Job Approved",
            message=f"Your job posting '{job.title}' has been approved.",
            notif_type="job_approved",
            link=f"/company/jobs/{job.id}",
        )
        AuditLog.log(
            action="job_approved",
            user_id=admin_id,
            entity_type="job",
            entity_id=job.id,
        )
        db.session.commit()
        cache.delete("admin_dashboard_stats")
        return job

    @staticmethod
    def reject_job(job_id: int, reason: str, admin_id: int) -> Job:
        job = Job.query.options(joinedload(Job.company)).get_or_404(job_id)
        job.reject(reason=reason)
        db.session.commit()

        Notification.create(
            user_id=job.company.user_id,
            title="Job Rejected",
            message=f"Your job '{job.title}' was rejected. Reason: {reason}",
            notif_type="job_rejected",
        )
        AuditLog.log(
            action="job_rejected",
            user_id=admin_id,
            entity_type="job",
            entity_id=job.id,
            details=reason,
        )
        db.session.commit()
        cache.delete("admin_dashboard_stats")
        return job

    @staticmethod
    def search_companies(
        q: str | None = None,
        industry: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ):
        query = Company.query.filter(Company.deleted_at.is_(None))
        if q:
            query = query.filter(
                or_(
                    Company.name.ilike(f"%{q}%"),
                    Company.location.ilike(f"%{q}%"),
                )
            )
        if industry:
            query = query.filter(Company.industry.ilike(f"%{industry}%"))

        return query.order_by(Company.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def search_students(
        q: str | None = None,
        branch: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ):
        query = Student.query.filter(Student.deleted_at.is_(None))
        if q:
            query = query.filter(
                or_(
                    Student.full_name.ilike(f"%{q}%"),
                    Student.student_id.ilike(f"%{q}%"),
                    Student.phone.ilike(f"%{q}%"),
                )
            )
        if branch:
            query = query.filter(Student.branch.ilike(f"%{branch}%"))

        return query.order_by(Student.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def blacklist_user(
        target_user_id: int,
        admin_id: int,
        reason: str,
        action: str = "blacklist",
    ) -> User:
        user = User.query.get_or_404(target_user_id)
        if user.role == "admin":
            raise ValueError("Cannot blacklist an admin")

        user.is_blacklisted = action == "blacklist"
        user.blacklist_reason = reason if action == "blacklist" else None
        if action == "blacklist":
            user.status = "blacklisted"

        log = BlacklistLog(
            admin_id=admin_id,
            target_user_id=target_user_id,
            reason=reason,
            action=action,
        )
        db.session.add(log)
        db.session.commit()

        AuditLog.log(
            action=f"user_{action}",
            user_id=admin_id,
            entity_type="user",
            entity_id=target_user_id,
            details=reason,
        )
        db.session.commit()
        return user
