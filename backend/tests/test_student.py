"""
Tests for student endpoints: dashboard, profile, resume upload, job search, apply, applications, placements.
"""

import io
import pytest
from flask.testing import FlaskClient
from backend.models import Application


def test_student_dashboard(client: FlaskClient, student_auth_headers, student_user):
    resp = client.get("/api/v1/student/dashboard", headers=student_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["student"]["id"] == student_user.student_profile.id
    assert "open_jobs" in data
    assert "recent_applications" in data


def test_get_student_profile(client: FlaskClient, student_auth_headers, student_user):
    resp = client.get("/api/v1/student/profile", headers=student_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["full_name"] == "Test Student"


def test_update_student_profile(
    client: FlaskClient, student_auth_headers, student_user
):
    resp = client.put(
        "/api/v1/student/profile",
        headers=student_auth_headers,
        json={"full_name": "Updated Name", "cgpa": 9.0},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["full_name"] == "Updated Name"
    assert data["cgpa"] == 9.0


def test_upload_resume(client: FlaskClient, student_auth_headers, student_user):
    data = {"resume": (io.BytesIO(b"dummy pdf content"), "resume.pdf")}
    resp = client.post(
        "/api/v1/student/profile/resume",
        headers=student_auth_headers,
        data=data,
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    json = resp.get_json()
    assert "resume_path" in json


def test_search_jobs(client: FlaskClient, student_auth_headers, approved_job):
    resp = client.get("/api/v1/student/jobs?q=Software", headers=student_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert any(j["title"] == "Software Engineer" for j in data["items"])


def test_apply_to_job(client: FlaskClient, student_auth_headers, approved_job):
    resp = client.post(
        f"/api/v1/student/jobs/{approved_job.id}/apply",
        headers=student_auth_headers,
        json={"cover_letter": "I am interested"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["status"] == "applied"
    assert data["job_id"] == approved_job.id


def test_my_applications(client: FlaskClient, student_auth_headers, application):
    resp = client.get("/api/v1/student/applications", headers=student_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1
    assert any(a["id"] == application.id for a in data)


def test_my_placements(
    client: FlaskClient, student_auth_headers, db, student_user, approved_job
):
    # Create a placement for the student
    from backend.models import Placement

    placement = Placement(
        job_id=approved_job.id,
        student_id=student_user.student_profile.id,
        offered_salary="10 LPA",
    )
    db.session.add(placement)
    db.session.commit()

    resp = client.get("/api/v1/student/placements", headers=student_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["job_id"] == approved_job.id
