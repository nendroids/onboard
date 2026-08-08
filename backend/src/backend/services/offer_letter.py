# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: offer letters                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from backend.models import Placement, Student, Job, Company


class OfferLetterService:

    @staticmethod
    def generate_text(placement: Placement) -> str:
        student = placement.student
        job = placement.job
        company = job.company

        return f"""
            OFFER LETTER

            Date: {datetime.now().strftime('%d %B %Y')}

            Dear {student.full_name},
            We are pleased to offer you the position of {job.title} at {company.name}.
            Package: {placement.ctc_offered or placement.offered_salary or 'As discussed'}
            Joining Date: {placement.joining_date.strftime('%d %B %Y') if placement.joining_date else 'To be decided'}

            Please confirm your acceptance at the earliest.

            Regards,
            {company.hr_name or 'HR Team'}
            {company.name}
            """
