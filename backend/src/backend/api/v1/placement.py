# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: placement                                                                                    │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
import os

from . import api_v1
from backend.utils.decorators import role_required, get_current_user
from backend.services import PlacementService
from backend.schemas import PlacementSchema
from backend.models import Placement, Job
from backend.extensions import cache


@api_v1.get("/admin/placements")
@jwt_required()
@role_required("admin")
@cache.cached(timeout=180, query_string=True)
def list_placements():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    query = Placement.query.options(
        joinedload(Placement.student),
        joinedload(Placement.job).joinedload(Job.company),
    )
    pagination = query.order_by(Placement.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return (
        jsonify(
            {
                "items": PlacementSchema(many=True).dump(pagination.items),
                "total": pagination.total,
                "page": pagination.page,
                "pages": pagination.pages,
            }
        ),
        200,
    )


@api_v1.get("/admin/placements/stats")
@jwt_required()
@role_required("admin")
@cache.cached(timeout=300)
def placement_stats():
    return jsonify(PlacementService.get_stats()), 200


@api_v1.get("/student/placements/<int:placement_id>/offer-letter")
@jwt_required()
@role_required("student")
def download_offer_letter(placement_id):
    user = get_current_user()
    placement = Placement.query.filter_by(
        id=placement_id, student_id=user.student_profile.id
    ).first_or_404()

    try:
        path = PlacementService.get_or_generate_offer_letter(placement.id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not os.path.exists(path):
        return jsonify({"error": "Offer letter not available"}), 404

    return send_file(path, as_attachment=True, download_name=os.path.basename(path))
