# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ v1: auth                                                                                         │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from marshmallow import ValidationError

from . import api_v1
from backend.services import AuthService
from backend.schemas import UserRegisterSchema, UserLoginSchema, UserSchema
from backend.models import User


@api_v1.post("/auth/register/student")
def register_student():
    try:
        data = UserRegisterSchema().load(request.get_json() or {})
        data["role"] = "student"
        result = AuthService.register_student(data)
        return (
            jsonify(
                {
                    **result,
                    "message": result.get("message", "Student registered successfully"),
                }
            ),
            201,
        )
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_v1.post("/auth/register/company")
def register_company():
    try:
        data = UserRegisterSchema().load(request.get_json() or {})
        data["role"] = "company"
        result = AuthService.register_company(data)
        return (
            jsonify(
                {
                    **result,
                    "message": result.get(
                        "message", "Company registered. Awaiting admin approval."
                    ),
                }
            ),
            201,
        )
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_v1.post("/auth/login")
def login():
    try:
        data = UserLoginSchema().load(request.get_json() or {})
        result = AuthService.login(data["email"], data["password"])
        return jsonify(result), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@api_v1.get("/auth/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(UserSchema().dump(user)), 200


@api_v1.post("/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.get(int(identity))
    claims = {"role": user.role, "status": user.status} if user else {}
    return (
        jsonify(
            {
                "access_token": create_access_token(
                    identity=str(identity), additional_claims=claims
                )
            }
        ),
        200,
    )
