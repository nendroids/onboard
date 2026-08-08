# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: cache                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from backend.extensions import cache


class CacheService:
    DASHBOARD_TTL = 60
    JOB_LIST_TTL = 120
    SEARCH_TTL = 90

    @staticmethod
    def invalidate_admin_stats() -> None:
        cache.delete("admin_dashboard_stats")

    @staticmethod
    def invalidate_job_list() -> None:
        from backend.services.job import JobService

        cache.delete_memoized(JobService.get_jobs)

    @staticmethod
    def invalidate_job_search() -> None:
        from backend.services.job import JobService

        cache.delete_memoized(JobService.search_jobs)

    @staticmethod
    def invalidate_all_job_cache() -> None:
        CacheService.invalidate_job_list()
        CacheService.invalidate_job_search()
        CacheService.invalidate_admin_stats()
