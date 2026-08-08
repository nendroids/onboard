"""
Unit tests for service layer methods (isolated from HTTP).
"""

import pytest
from backend.services.auth import AuthService
from backend.services.admin import AdminService
from backend.services.company import CompanyService
from backend.services.student import StudentService
from backend.models import User, Company, Job, Application
from backend.extensions import db


def test_auth_register_student(db):
    data = {
        "username": "svcstudent",
        "email": "svc@example.com",
        "password": "pass123",
        "role": "student",
    }
    result = AuthService.register_student(data)
    assert "access_token" in result
    user = User.query.filter_by(email="svc@example.com").first()
    assert user is not None
    assert user.student_profile is not None
    assert user.student_profile.full_name == "svcstudent"  # fallback


def test_auth_login(db, student_user):
    result = AuthService.login(student_user.email, "studentpass")
    assert "access_token" in result


def test_admin_dashboard_stats(db, admin_user):
    stats = AdminService.get_dashboard_stats()
    assert "users" in stats
    assert "companies" in stats
    assert "jobs" in stats


def test_admin_approve_company(db, company_user):
    company = company_user.company_profile
    # Initially approved, but we can test reject/approve logic
    company.approved_at = None  # set as pending
    db.session.commit()
    updated = AdminService.approve_company(
        company.id, admin_user_id=1
    )  # assuming admin id exists
    assert updated.is_approved is True


def test_company_create_job(db, company_user):
    company = company_user.company_profile
    data = {"title": "Service Job", "description": "Test", "openings": 3}
    job = CompanyService.create_job(company.id, data)
    assert job.title == "Service Job"
    assert job.status == "pending"


def test_student_apply_to_job(db, student_user, approved_job):
    student = student_user.student_profile
    app = StudentService.apply_to_job(student.id, approved_job.id, cover_letter="Hello")
    assert app is not None
    assert app.status == "applied"
    assert app.cover_letter == "Hello"


def test_student_get_dashboard(db, student_user):
    student = student_user.student_profile
    data = StudentService.get_dashboard(student.id)
    assert data["student"] == student
    assert "open_jobs" in data
    assert "recent_applications" in data
