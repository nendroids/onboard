"""
Tests for application detail endpoint (permissions).
"""

import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token


def test_get_application_as_student(
    client: FlaskClient, student_auth_headers, application
):
    resp = client.get(
        f"/api/v1/applications/{application.id}", headers=student_auth_headers
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == application.id
    assert data["status"] == "applied"


def test_get_application_as_company(
    client: FlaskClient, company_auth_headers, application
):
    resp = client.get(
        f"/api/v1/applications/{application.id}", headers=company_auth_headers
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == application.id


def test_get_application_forbidden_other_student(
    client: FlaskClient, student_token, application, db
):
    # Create another student
    from backend.models import User, Student

    other_user = User(
        username="other", email="other@example.com", role="student", status="approved"
    )
    other_user.set_password("pass")
    db.session.add(other_user)
    db.session.flush()
    other_student = Student(
        user_id=other_user.id, full_name="Other", student_id="OTH", branch="ECE"
    )
    db.session.add(other_student)
    db.session.commit()

    other_token = create_access_token(
        identity=str(other_user.id),
        additional_claims={"role": other_user.role, "status": other_user.status},
    )
    headers = {"Authorization": f"Bearer {other_token}"}
    resp = client.get(f"/api/v1/applications/{application.id}", headers=headers)
    assert resp.status_code == 403
    assert "error" in resp.get_json()
