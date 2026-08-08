# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: company                                                                                      │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from . import api_v1
from backend.utils.decorators import role_required, get_current_user
from backend.services import CompanyService
from backend.schemas import (
    CompanySchema,
    CompanyUpdateSchema,
    JobSchema,
    JobCreateSchema,
    JobUpdateSchema,
    ApplicationSchema,
    ApplicationStatusUpdateSchema,
    InterviewSchema,
    InterviewCreateSchema,
    PlacementSchema,
)
from backend.models import Job
from backend.extensions import db


@api_v1.get("/company/dashboard")
@jwt_required()
@role_required("company")
def company_dashboard():
    user = get_current_user()
    if not user.company_profile:
        return jsonify({"error": "Company profile not found"}), 404
    try:
        data = CompanyService.get_dashboard(user.company_profile.id)
        return (
            jsonify(
                {
                    "company": CompanySchema().dump(data["company"]),
                    "jobs": JobSchema(many=True).dump(data["jobs"]),
                    "stats": data["stats"],
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 403


@api_v1.route("/company/profile", methods=["GET", "PUT"])
@jwt_required()
@role_required("company")
def company_profile():
    user = get_current_user()
    company = user.company_profile
    if not company:
        return jsonify({"error": "Company profile not found"}), 404

    if request.method == "GET":
        return jsonify(CompanySchema().dump(company)), 200

    try:
        data = CompanyUpdateSchema().load(request.get_json() or {})
        for k, v in data.items():
            setattr(company, k, v)
        db.session.commit()
        return jsonify(CompanySchema().dump(company)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400


@api_v1.route("/company/jobs", methods=["GET", "POST"])
@jwt_required()
@role_required("company")
def company_jobs():
    user = get_current_user()
    company = user.company_profile
    if not company:
        return jsonify({"error": "Company profile not found"}), 404

    if request.method == "GET":
        jobs = (
            company.jobs.filter(Job.deleted_at.is_(None))
            .order_by(Job.created_at.desc())
            .all()
        )
        return jsonify(JobSchema(many=True).dump(jobs)), 200

    try:
        data = JobCreateSchema().load(request.get_json() or {})
        job = CompanyService.create_job(company.id, data)
        return jsonify(JobSchema().dump(job)), 201
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.route("/company/jobs/<int:job_id>", methods=["GET", "PUT"])
@jwt_required()
@role_required("company")
def company_job_detail(job_id):
    user = get_current_user()
    company = user.company_profile

    if request.method == "GET":
        job = Job.query.filter_by(id=job_id, company_id=company.id).first_or_404()
        return jsonify(JobSchema().dump(job)), 200

    try:
        data = JobUpdateSchema().load(request.get_json() or {})
        job = CompanyService.update_job(job_id, company.id, data)
        return jsonify(JobSchema().dump(job)), 200
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.get("/company/jobs/<int:job_id>/applicants")
@jwt_required()
@role_required("company")
def job_applicants(job_id):
    user = get_current_user()
    status = request.args.get("status")
    applicants = CompanyService.get_applicants(job_id, user.company_profile.id, status)
    return jsonify(ApplicationSchema(many=True).dump(applicants)), 200


@api_v1.patch("/company/applications/<int:app_id>/status")
@jwt_required()
@role_required("company")
def update_application_status(app_id):
    user = get_current_user()
    try:
        data = ApplicationStatusUpdateSchema().load(request.get_json() or {})
        app = CompanyService.update_application_status(
            app_id, user.company_profile.id, data["status"], data.get("feedback")
        )
        return jsonify(ApplicationSchema().dump(app)), 200
    except (ValidationError, ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.post("/company/applications/<int:app_id>/interview")
@jwt_required()
@role_required("company")
def schedule_interview(app_id):
    user = get_current_user()
    try:
        data = InterviewCreateSchema().load(request.get_json() or {})
        interview = CompanyService.schedule_interview(
            app_id,
            user.company_profile.id,
            data["scheduled_at"],
            mode=data.get("mode"),
            link=data.get("link"),
            location=data.get("location"),
        )
        return jsonify(InterviewSchema().dump(interview)), 201
    except (ValidationError, ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.post("/company/applications/<int:app_id>/select")
@jwt_required()
@role_required("company")
def select_candidate(app_id):
    user = get_current_user()
    data = request.get_json() or {}
    try:
        placement = CompanyService.select_candidate(
            app_id,
            user.company_profile.id,
            offered_salary=data.get("offered_salary"),
            ctc_offered=data.get("ctc_offered"),
            joining_date=data.get("joining_date"),
        )
        return jsonify(PlacementSchema().dump(placement)), 201
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 400
