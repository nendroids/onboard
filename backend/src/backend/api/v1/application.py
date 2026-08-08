# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: application                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import jsonify
from flask_jwt_extended import jwt_required

from . import api_v1
from backend.utils.decorators import get_current_user
from backend.models import Application
from backend.schemas import ApplicationSchema


@api_v1.get("/applications/<int:app_id>")
@jwt_required()
def get_application(app_id):
    user = get_current_user()
    app = Application.query.get_or_404(app_id)

    if user.role == "student" and app.student.user_id != user.id:
        return jsonify({"error": "Forbidden"}), 403
    if user.role == "company" and app.job.company.user_id != user.id:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify(ApplicationSchema().dump(app)), 200
