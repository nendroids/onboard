# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: eligibility                                                                            │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from backend.models import Student, Job


class EligibilityService:

    @staticmethod
    def check(student: Student, job: Job) -> None:
        errors: list[str] = []

        if job.min_cgpa is not None and student.cgpa is not None:
            if student.cgpa < job.min_cgpa:
                errors.append(
                    f"Minimum CGPA required is {job.min_cgpa}, your CGPA is {student.cgpa}"
                )

        if job.eligible_branches:
            allowed = {b.strip().lower() for b in job.eligible_branches.split(",")}
            if student.branch and student.branch.strip().lower() not in allowed:
                errors.append(
                    f"Your branch '{student.branch}' is not eligible. Allowed: {job.eligible_branches}"
                )

        if job.eligible_year is not None and student.graduation_year is not None:
            if student.graduation_year != job.eligible_year:
                errors.append(
                    f"Only students graduating in {job.eligible_year} are eligible"
                )

        if errors:
            raise ValueError("; ".join(errors))

    @staticmethod
    def is_eligible(student: Student, job: Job) -> bool:
        try:
            EligibilityService.check(student, job)
            return True
        except ValueError:
            return False
