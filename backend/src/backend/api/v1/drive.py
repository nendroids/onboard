# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: drive                                                                                        │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify
from sqlalchemy.orm import joinedload

from . import api_v1
from backend.models import Job
from backend.schemas import JobSchema
from backend.extensions import cache


@api_v1.get("/drives")
@cache.cached(timeout=90, query_string=True)
def list_approved_drives():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 50)
    q = request.args.get("q")

    query = (
        Job.query.filter_by(status="approved")
        .filter(Job.deleted_at.is_(None))
        .options(joinedload(Job.company))
    )
    if q:
        query = query.filter(Job.title.ilike(f"%{q}%"))

    pagination = query.order_by(Job.deadline.asc().nullslast()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return (
        jsonify(
            {
                "items": JobSchema(many=True).dump(pagination.items),
                "total": pagination.total,
                "page": pagination.page,
                "pages": pagination.pages,
            }
        ),
        200,
    )


@api_v1.get("/drives/<int:job_id>")
def get_drive(job_id):
    job = (
        Job.query.filter_by(id=job_id, status="approved")
        .filter(Job.deleted_at.is_(None))
        .options(joinedload(Job.company))
        .first_or_404()
    )
    return jsonify(JobSchema().dump(job)), 200
