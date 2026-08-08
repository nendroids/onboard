# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: placement                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯


import os
from sqlalchemy import func

from backend.extensions import db, cache
from backend.models import Placement, Student
from backend.services.offer_letter import OfferLetterService


class PlacementService:

    @staticmethod
    def get_stats():
        total = Placement.query.count()
        avg_ctc = db.session.query(func.avg(Placement.ctc_offered)).scalar() or 0
        highest_ctc = db.session.query(func.max(Placement.ctc_offered)).scalar() or 0

        by_branch = (
            db.session.query(Student.branch, func.count(Placement.id))
            .join(Placement, Placement.student_id == Student.id)
            .group_by(Student.branch)
            .all()
        )

        return {
            "total_placements": total,
            "average_ctc": float(avg_ctc),
            "highest_ctc": float(highest_ctc),
            "by_branch": {branch: count for branch, count in by_branch},
        }

    @staticmethod
    def get_or_generate_offer_letter(placement_id):
        placement = Placement.query.get(placement_id)
        if not placement:
            raise ValueError("Placement not found")

        if placement.offer_letter_path and os.path.exists(placement.offer_letter_path):
            return placement.offer_letter_path

        path = OfferLetterService.generate(placement)
        placement.offer_letter_path = path
        db.session.commit()
        cache.delete("view//api/v1/admin/placements")
        return path
