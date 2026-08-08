# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: interview                                                                                    │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload

from . import api_v1
from backend.utils.decorators import role_required, get_current_user
from backend.services import InterviewService
from backend.schemas import InterviewSchema, InterviewUpdateSchema
from backend.models import Interview, Application, Job


@api_v1.get("/student/interviews")
@jwt_required()
@role_required("student")
def student_interviews():
    user = get_current_user()
    status = request.args.get("status")

    query = (
        Interview.query.join(Application)
        .filter(Application.student_id == user.student_profile.id)
        .options(
            joinedload(Interview.application)
            .joinedload(Application.job)
            .joinedload(Job.company)
        )
    )
    if status:
        query = query.filter(Interview.status == status)

    interviews = query.order_by(Interview.scheduled_at.asc()).all()
    return jsonify(InterviewSchema(many=True).dump(interviews)), 200


@api_v1.get("/company/interviews")
@jwt_required()
@role_required("company")
def company_interviews():
    user = get_current_user()
    company = user.company_profile
    if not company:
        return jsonify({"error": "Company profile not found"}), 404

    job_id = request.args.get("job_id", type=int)
    status = request.args.get("status")

    query = (
        Interview.query.join(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(Job.company_id == company.id)
        .options(joinedload(Interview.application).joinedload(Application.student))
    )
    if job_id:
        query = query.filter(Job.id == job_id)
    if status:
        query = query.filter(Interview.status == status)

    interviews = query.order_by(Interview.scheduled_at.asc()).all()
    return jsonify(InterviewSchema(many=True).dump(interviews)), 200


@api_v1.patch("/company/interviews/<int:interview_id>")
@jwt_required()
@role_required("company")
def update_interview(interview_id):
    user = get_current_user()
    try:
        data = InterviewUpdateSchema().load(request.get_json() or {})
        interview = InterviewService.update_interview(
            interview_id, user.company_profile.id, data
        )
        return jsonify(InterviewSchema().dump(interview)), 200
    except (ValidationError, ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400
