# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ utils: decorators                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from functools import wraps
from flask import abort, jsonify, request
from flask_login import current_user
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from backend.models import User
from backend.extensions import cache


def role_required(*roles):

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"error": "Forbidden – insufficient permissions"}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def login_role_required(*roles):

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.is_blacklisted:
                abort(403)
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)

        return decorated

    return decorator


def jwt_role_required(*roles):

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if not user or user.is_blacklisted or user.role not in roles:
                return jsonify({"error": "Unauthorized"}), 403
            return f(*args, **kwargs)

        return decorated

    return decorator


def get_current_user() -> User:
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.is_blacklisted:
        raise PermissionError("User not found or blacklisted")
    return user


def cache_response(timeout: int = 300):

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = f"resp:{request.path}:{request.query_string.decode()}"
            cached = cache.get(key)
            if cached is not None:
                return cached
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                data, status = response[0], response[1] if len(response) > 1 else 200
                if status == 200:
                    cache.set(key, response, timeout=timeout)
            else:
                cache.set(key, response, timeout=timeout)
            return response

        return decorated

    return decorator
