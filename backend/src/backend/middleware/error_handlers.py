# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ middleware: error handlers                                                                       │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

import logging
import traceback

from datetime import datetime, timezone
from typing import Any
from flask import Flask, current_app, jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

_STATUS_MESSAGES: dict[int, tuple[str, str]] = {
    400: ("Bad Request", "The request contains invalid or missing data."),
    401: ("Unauthorized", "Authentication is required to access this resource."),
    403: ("Forbidden", "You do not have permission to perform this action."),
    404: ("Not Found", "The requested resource could not be found."),
    405: (
        "Method Not Allowed",
        "The requested HTTP method is not allowed for this endpoint.",
    ),
    406: ("Not Acceptable", "The requested response format is not supported."),
    409: ("Conflict", "The request conflicts with the current state of the resource."),
    413: ("Payload Too Large", "The uploaded file exceeds the maximum allowed size."),
    415: ("Unsupported Media Type", "The uploaded file type is not supported."),
    422: ("Unprocessable Entity", "The submitted data failed validation."),
    429: ("Too Many Requests", "Too many requests. Please try again later."),
    500: ("Internal Server Error", "An unexpected server error occurred."),
    502: ("Bad Gateway", "An upstream service returned an invalid response."),
    503: (
        "Service Unavailable",
        "The service is temporarily unavailable. Please try again later.",
    ),
    504: ("Gateway Timeout", "The request to an upstream service timed out."),
}


def _error_response(
    *,
    status_code: int,
    error: str,
    message: str,
    details: Any | None = None,
):
    body: dict[str, Any] = {
        "success": False,
        "status": status_code,
        "error": error,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": request.path,
        "method": request.method,
    }
    if details is not None:
        body["details"] = details
    return jsonify(body), status_code


def _http_exception_handler(exc: HTTPException):
    code = exc.code or 500
    name, default_msg = _STATUS_MESSAGES.get(
        code, (exc.name or "HTTP Error", "An HTTP error occurred.")
    )
    message = exc.description or default_msg
    if code >= 500:
        logger.exception(
            "HTTP %s on %s %s",
            code,
            request.method,
            request.path,
        )
    return _error_response(status_code=code, error=name, message=message)


def _unhandled_exception_handler(exc: Exception):
    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.path,
    )

    if current_app.debug:
        details = traceback.format_exc()
        message = str(exc)
    else:
        details = None
        message = "An unexpected server error occurred."

    return _error_response(
        status_code=500,
        error="Internal Server Error",
        message=message,
        details=details,
    )


def register_error_handlers(app: Flask) -> None:
    for code in _STATUS_MESSAGES:
        app.register_error_handler(code, _http_exception_handler)
    app.register_error_handler(HTTPException, _http_exception_handler)
    app.register_error_handler(Exception, _unhandled_exception_handler)
