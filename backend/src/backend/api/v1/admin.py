# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: admin                                                                                        │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from . import api_v1
from backend.utils.decorators import role_required, get_current_user
from backend.services import AdminService
from backend.schemas import (
    CompanySchema,
    StudentSchema,
    JobSchema,
    CompanyApprovalSchema,
    JobApprovalSchema,
    ApplicationSchema,
)
from backend.models import Job, Application


@api_v1.get("/admin/dashboard")
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({"stats": AdminService.get_dashboard_stats()}), 200


@api_v1.get("/admin/companies")
@jwt_required()
@role_required("admin")
def list_companies():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    pagination = AdminService.search_companies(
        q=request.args.get("q"),
        industry=request.args.get("industry"),
        page=page,
        per_page=per_page,
    )
    return (
        jsonify(
            {
                "items": CompanySchema(many=True).dump(pagination.items),
                "total": pagination.total,
                "page": pagination.page,
                "pages": pagination.pages,
            }
        ),
        200,
    )


@api_v1.post("/admin/companies/<int:company_id>/approve")
@jwt_required()
@role_required("admin")
def approve_company(company_id):
    admin = get_current_user()
    try:
        data = CompanyApprovalSchema().load(request.get_json() or {})
        if data["action"] == "approve":
            company = AdminService.approve_company(company_id, admin.id)
        else:
            company = AdminService.reject_company(
                company_id, data.get("rejection_reason", ""), admin.id
            )
        return jsonify(CompanySchema().dump(company)), 200
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.get("/admin/jobs")
@jwt_required()
@role_required("admin")
def list_jobs():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    status = request.args.get("status")

    query = Job.query.filter(Job.deleted_at.is_(None))
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Job.created_at.desc()).paginate(
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


@api_v1.post("/admin/jobs/<int:job_id>/approve")
@jwt_required()
@role_required("admin")
def approve_job(job_id):
    admin = get_current_user()
    try:
        data = JobApprovalSchema().load(request.get_json() or {})
        if data["action"] == "approve":
            job = AdminService.approve_job(job_id, admin.id)
        else:
            job = AdminService.reject_job(
                job_id, data.get("rejection_reason", ""), admin.id
            )
        return jsonify(JobSchema().dump(job)), 200
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.get("/admin/students")
@jwt_required()
@role_required("admin")
def list_students():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    pagination = AdminService.search_students(
        q=request.args.get("q"),
        branch=request.args.get("branch"),
        page=page,
        per_page=per_page,
    )
    return (
        jsonify(
            {
                "items": StudentSchema(many=True).dump(pagination.items),
                "total": pagination.total,
                "page": pagination.page,
                "pages": pagination.pages,
            }
        ),
        200,
    )


@api_v1.post("/admin/users/<int:user_id>/blacklist")
@jwt_required()
@role_required("admin")
def blacklist_user(user_id):
    admin = get_current_user()
    data = request.get_json() or {}
    try:
        user = AdminService.blacklist_user(
            user_id,
            admin.id,
            reason=data.get("reason", "No reason provided"),
            action=data.get("action", "blacklist"),
        )
        return (
            jsonify(
                {
                    "message": f"User {data.get('action', 'blacklist')}ed",
                    "user_id": user.id,
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_v1.get("/admin/applications")
@jwt_required()
@role_required("admin")
def list_all_applications():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    status = request.args.get("status")

    query = Application.query.filter(Application.deleted_at.is_(None))
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Application.applied_on.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return (
        jsonify(
            {
                "items": ApplicationSchema(many=True).dump(pagination.items),
                "total": pagination.total,
                "page": pagination.page,
                "pages": pagination.pages,
            }
        ),
        200,
    )
