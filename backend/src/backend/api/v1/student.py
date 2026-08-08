# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: student                                                                                      │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import os

from . import api_v1
from backend.utils.decorators import role_required, get_current_user
from backend.services import StudentService
from backend.schemas import (
    StudentSchema,
    StudentUpdateSchema,
    JobSchema,
    ApplicationSchema,
    ApplicationCreateSchema,
    PlacementSchema,
)
from backend.extensions import db


@api_v1.get("/student/dashboard")
@jwt_required()
@role_required("student")
def student_dashboard():
    user = get_current_user()
    if not user.student_profile:
        return jsonify({"error": "Student profile not found"}), 404
    data = StudentService.get_dashboard(user.student_profile.id)
    return (
        jsonify(
            {
                "student": StudentSchema().dump(data["student"]),
                "open_jobs": JobSchema(many=True).dump(data["open_jobs"]),
                "recent_applications": ApplicationSchema(many=True).dump(
                    data["recent_applications"]
                ),
                "active_count": data["active_count"],
                "is_placed": data["is_placed"],
            }
        ),
        200,
    )


@api_v1.route("/student/profile", methods=["GET", "PUT"])
@jwt_required()
@role_required("student")
def student_profile():
    user = get_current_user()
    student = user.student_profile
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    if request.method == "GET":
        return jsonify(StudentSchema().dump(student)), 200

    try:
        data = StudentUpdateSchema().load(request.get_json() or {})
        student = StudentService.update_profile(student.id, data)
        return jsonify(StudentSchema().dump(student)), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400


@api_v1.post("/student/profile/resume")
@jwt_required()
@role_required("student")
def upload_resume():
    user = get_current_user()
    student = user.student_profile
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if not file.filename or not file.filename.lower().endswith(
        (".pdf", ".doc", ".docx")
    ):
        return jsonify({"error": "Only PDF/DOC/DOCX allowed"}), 400

    filename = secure_filename(f"resume_{student.id}_{file.filename}")
    upload_dir = os.path.join("uploads", "resumes")
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, filename)
    file.save(path)

    student.resume_path = path
    db.session.commit()
    return jsonify({"message": "Resume uploaded", "resume_path": path}), 200


@api_v1.get("/student/jobs")
@jwt_required()
@role_required("student")
def search_jobs():
    user = get_current_user()
    pagination = StudentService.search_jobs(
        user.student_profile.id,
        q=request.args.get("q"),
        skills=request.args.get("skills"),
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 12, type=int), 50),
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


@api_v1.post("/student/jobs/<int:job_id>/apply")
@jwt_required()
@role_required("student")
def apply_to_job(job_id):
    user = get_current_user()
    try:
        data = ApplicationCreateSchema().load(request.get_json() or {})
        application = StudentService.apply_to_job(
            user.student_profile.id, job_id, cover_letter=data.get("cover_letter")
        )
        return jsonify(ApplicationSchema().dump(application)), 201
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@api_v1.get("/student/applications")
@jwt_required()
@role_required("student")
def my_applications():
    user = get_current_user()
    apps = StudentService.get_my_applications(user.student_profile.id)
    return jsonify(ApplicationSchema(many=True).dump(apps)), 200


@api_v1.get("/student/placements")
@jwt_required()
@role_required("student")
def my_placements():
    user = get_current_user()
    placements = StudentService.get_placement_history(user.student_profile.id)
    return jsonify(PlacementSchema(many=True).dump(placements)), 200
