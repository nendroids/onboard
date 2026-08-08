# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: job                                                                                    │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from backend.extensions import cache
from backend.services.cache import CacheService
from backend.models import Job


class JobService:

    @staticmethod
    @cache.memoize(timeout=CacheService.JOB_LIST_TTL)
    def get_jobs(page: int = 1, per_page: int = 10, search: str | None = None):

        query = Job.query

        if search:
            query = query.filter(Job.title.ilike(f"%{search}%"))

        return query.order_by(Job.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )

    @staticmethod
    @cache.memoize(timeout=CacheService.SEARCH_TTL)
    def search_jobs(keyword: str):

        return (
            Job.query.filter(Job.title.ilike(f"%{keyword}%"))
            .order_by(Job.created_at.desc())
            .all()
        )

    @staticmethod
    def create_job(data: dict):

        job = Job(**data)

        from backend.extensions import db

        db.session.add(job)
        db.session.commit()

        CacheService.invalidate_all_job_cache()

        return job

    @staticmethod
    def update_job(job, data: dict):

        for key, value in data.items():
            setattr(job, key, value)

        from backend.extensions import db

        db.session.commit()

        CacheService.invalidate_all_job_cache()

        return job

    @staticmethod
    def delete_job(job):

        from backend.extensions import db

        db.session.delete(job)
        db.session.commit()

        CacheService.invalidate_all_job_cache()
