# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: export                                                                                       │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import jsonify, send_file
from flask_jwt_extended import jwt_required
import os

from . import api_v1
from backend.utils.decorators import role_required, get_current_user
from backend.services import ExportService
from backend.models import ExportJob


@api_v1.post("/student/exports")
@jwt_required()
@role_required("student")
def request_export():
    user = get_current_user()
    export_job = ExportService.request_export(user.student_profile.id)
    return (
        jsonify(
            {
                "message": "Export started. You will be notified when ready.",
                "export_id": export_job.id,
                "status": export_job.status,
            }
        ),
        202,
    )


@api_v1.get("/student/exports/<int:export_id>")
@jwt_required()
@role_required("student")
def get_export_status(export_id):
    user = get_current_user()
    export_job = ExportJob.query.filter_by(
        id=export_id, student_id=user.student_profile.id
    ).first_or_404()

    return (
        jsonify(
            {
                "id": export_job.id,
                "status": export_job.status,
                "file_path": export_job.file_path,
                "error_message": export_job.error_message,
                "requested_at": (
                    export_job.requested_at.isoformat()
                    if export_job.requested_at
                    else None
                ),
                "completed_at": (
                    export_job.completed_at.isoformat()
                    if export_job.completed_at
                    else None
                ),
            }
        ),
        200,
    )


@api_v1.get("/student/exports/<int:export_id>/download")
@jwt_required()
@role_required("student")
def download_export(export_id):
    user = get_current_user()
    export_job = ExportJob.query.filter_by(
        id=export_id, student_id=user.student_profile.id
    ).first_or_404()

    if export_job.status != "completed" or not export_job.file_path:
        return jsonify({"error": "Export not ready"}), 400
    if not os.path.exists(export_job.file_path):
        return jsonify({"error": "File missing"}), 404

    return send_file(
        export_job.file_path,
        as_attachment=True,
        download_name=os.path.basename(export_job.file_path),
    )
