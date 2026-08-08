"""
Tests for admin API endpoints: dashboard, companies, jobs, students, blacklist.
"""

import pytest
from flask.testing import FlaskClient
from backend.models import Company, Job, User


def test_admin_dashboard(client: FlaskClient, auth_headers):
    resp = client.get("/api/v1/admin/dashboard", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "stats" in data


def test_list_companies(client: FlaskClient, auth_headers, company_user):
    resp = client.get("/api/v1/admin/companies", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    items = data["items"]
    assert any(item["id"] == company_user.company_profile.id for item in items)


def test_approve_company(client: FlaskClient, auth_headers, db):
    # Create a pending company
    user = User(
        username="pendingco", email="pending@co.com", role="company", status="pending"
    )
    user.set_password("pass")
    db.session.add(user)
    db.session.flush()
    company = Company(user_id=user.id, name="Pending Corp")
    db.session.add(company)
    db.session.commit()

    resp = client.post(
        f"/api/v1/admin/companies/{company.id}/approve",
        headers=auth_headers,
        json={"action": "approve"},
    )
    assert resp.status_code == 200
    assert company.is_approved is True


def test_reject_company(client: FlaskClient, auth_headers, db):
    user = User(
        username="rejectco", email="reject@co.com", role="company", status="pending"
    )
    user.set_password("pass")
    db.session.add(user)
    db.session.flush()
    company = Company(user_id=user.id, name="Reject Corp")
    db.session.add(company)
    db.session.commit()

    resp = client.post(
        f"/api/v1/admin/companies/{company.id}/approve",
        headers=auth_headers,
        json={"action": "reject", "rejection_reason": "Not suitable"},
    )
    assert resp.status_code == 200
    assert company.is_approved is False
    assert company.rejection_reason == "Not suitable"


def test_list_jobs(client: FlaskClient, auth_headers, approved_job):
    resp = client.get("/api/v1/admin/jobs", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert any(j["id"] == approved_job.id for j in data["items"])


def test_approve_job(client: FlaskClient, auth_headers, pending_job, db):
    resp = client.post(
        f"/api/v1/admin/jobs/{pending_job.id}/approve",
        headers=auth_headers,
        json={"action": "approve"},
    )
    assert resp.status_code == 200
    db.session.refresh(pending_job)
    assert pending_job.status == "approved"


def test_reject_job(client: FlaskClient, auth_headers, pending_job, db):
    resp = client.post(
        f"/api/v1/admin/jobs/{pending_job.id}/approve",
        headers=auth_headers,
        json={"action": "reject", "rejection_reason": "Bad"},
    )
    assert resp.status_code == 200
    db.session.refresh(pending_job)
    assert pending_job.status == "rejected"
    assert pending_job.rejection_reason == "Bad"


def test_list_students(client: FlaskClient, auth_headers, student_user):
    resp = client.get("/api/v1/admin/students", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert any(s["id"] == student_user.student_profile.id for s in data["items"])


def test_blacklist_user(client: FlaskClient, auth_headers, student_user, db):
    resp = client.post(
        f"/api/v1/admin/users/{student_user.id}/blacklist",
        headers=auth_headers,
        json={"action": "blacklist", "reason": "Spam"},
    )
    assert resp.status_code == 200
    db.session.refresh(student_user)
    assert student_user.is_blacklisted is True
    assert student_user.blacklist_reason == "Spam"


def test_list_applications(client: FlaskClient, auth_headers, application):
    resp = client.get("/api/v1/admin/applications", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert any(a["id"] == application.id for a in data["items"])
