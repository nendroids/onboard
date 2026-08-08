"""
Tests for company endpoints: dashboard, profile, job CRUD, applicants, interviews, selection.
"""

import pytest
from flask.testing import FlaskClient
from backend.models import Job, Application


def test_company_dashboard(client: FlaskClient, company_auth_headers, company_user):
    resp = client.get("/api/v1/company/dashboard", headers=company_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["company"]["id"] == company_user.company_profile.id
    assert "jobs" in data
    assert "stats" in data


def test_get_company_profile(client: FlaskClient, company_auth_headers, company_user):
    resp = client.get("/api/v1/company/profile", headers=company_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == "Test Corp"


def test_update_company_profile(
    client: FlaskClient, company_auth_headers, company_user
):
    resp = client.put(
        "/api/v1/company/profile",
        headers=company_auth_headers,
        json={"name": "New Name", "industry": "Finance"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == "New Name"
    assert data["industry"] == "Finance"


def test_create_job(client: FlaskClient, company_auth_headers, company_user):
    data = {
        "title": "DevOps Engineer",
        "description": "Manage cloud",
        "openings": 2,
        "package_lpa": 15.0,
    }
    resp = client.post("/api/v1/company/jobs", headers=company_auth_headers, json=data)
    assert resp.status_code == 201
    json = resp.get_json()
    assert json["title"] == "DevOps Engineer"
    assert json["status"] == "pending"


def test_list_company_jobs(client: FlaskClient, company_auth_headers, approved_job):
    resp = client.get("/api/v1/company/jobs", headers=company_auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1
    assert any(j["id"] == approved_job.id for j in data)


def test_get_job_detail(client: FlaskClient, company_auth_headers, approved_job):
    resp = client.get(
        f"/api/v1/company/jobs/{approved_job.id}", headers=company_auth_headers
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == approved_job.id


def test_update_job(client: FlaskClient, company_auth_headers, pending_job):
    resp = client.put(
        f"/api/v1/company/jobs/{pending_job.id}",
        headers=company_auth_headers,
        json={"title": "Updated Title", "openings": 5},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["title"] == "Updated Title"
    assert data["openings"] == 5


def test_job_applicants(client: FlaskClient, company_auth_headers, application):
    resp = client.get(
        f"/api/v1/company/jobs/{application.job_id}/applicants",
        headers=company_auth_headers,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["id"] == application.id


def test_update_application_status(
    client: FlaskClient, company_auth_headers, application
):
    resp = client.patch(
        f"/api/v1/company/applications/{application.id}/status",
        headers=company_auth_headers,
        json={"status": "shortlisted", "feedback": "Good"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "shortlisted"
    assert data["feedback"] == "Good"


def test_schedule_interview(client: FlaskClient, company_auth_headers, application):
    resp = client.post(
        f"/api/v1/company/applications/{application.id}/interview",
        headers=company_auth_headers,
        json={
            "scheduled_at": "2026-08-10T10:00:00Z",
            "mode": "video",
            "link": "https://meet.google.com/abc",
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["mode"] == "video"
    assert data["link"] == "https://meet.google.com/abc"


def test_select_candidate(client: FlaskClient, company_auth_headers, application):
    resp = client.post(
        f"/api/v1/company/applications/{application.id}/select",
        headers=company_auth_headers,
        json={"offered_salary": "12 LPA", "ctc_offered": "15 LPA"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["job_id"] == application.job_id
    assert data["student_id"] == application.student_id
