"""
Tests for authentication endpoints: registration, login, refresh, and me.
"""

import pytest
from flask.testing import FlaskClient
from backend.models import User


def test_register_student_success(client: FlaskClient, db):
    data = {
        "username": "newstudent",
        "email": "new@example.com",
        "password": "pass123",
        "role": "student",
        "student_id": "S12345",  # required
        "full_name": "New Student",  # required
        "branch": "CSE",
        "cgpa": 8.5,
        "graduation_year": 2026,
    }
    resp = client.post("/api/v1/auth/register/student", json=data)
    assert resp.status_code == 201
    json = resp.get_json()
    assert "access_token" in json
    assert "refresh_token" in json
    user = User.query.filter_by(email="new@example.com").first()
    assert user is not None
    assert user.role == "student"
    assert user.student_profile is not None


def test_register_company_success(client: FlaskClient, db):
    data = {
        "username": "newcompany",
        "email": "company@test.com",
        "password": "compass",
        "role": "company",
        "name": "Test Corp",  # required
        "industry": "Technology",
    }
    resp = client.post("/api/v1/auth/register/company", json=data)
    assert resp.status_code == 201
    json = resp.get_json()
    assert "access_token" in json
    user = User.query.filter_by(email="company@test.com").first()
    assert user.company_profile is not None


def test_register_duplicate_email(client: FlaskClient, db, student_user):
    data = {
        "username": "duplicate",
        "email": student_user.email,
        "password": "pass",
        "role": "student",
        "student_id": "DUP",
        "full_name": "Duplicate",
        "branch": "CSE",
        "cgpa": 7.0,
        "graduation_year": 2026,
    }
    resp = client.post("/api/v1/auth/register/student", json=data)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_login_success(client: FlaskClient, student_user):
    data = {"email": student_user.email, "password": "studentpass"}
    resp = client.post("/api/v1/auth/login", json=data)
    assert resp.status_code == 200
    json = resp.get_json()
    assert "access_token" in json
    assert "refresh_token" in json


def test_login_wrong_password(client: FlaskClient, student_user):
    data = {"email": student_user.email, "password": "wrong"}
    resp = client.post("/api/v1/auth/login", json=data)
    assert resp.status_code == 401
    assert "error" in resp.get_json()


def test_me_endpoint(client: FlaskClient, student_token):
    headers = {"Authorization": f"Bearer {student_token}"}
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    json = resp.get_json()
    assert json["email"] == "student@example.com"
    assert json["role"] == "student"


def test_refresh_token(client: FlaskClient, student_user):
    data = {"email": student_user.email, "password": "studentpass"}
    resp = client.post("/api/v1/auth/login", json=data)
    refresh_token = resp.get_json()["refresh_token"]
    headers = {"Authorization": f"Bearer {refresh_token}"}
    resp = client.post("/api/v1/auth/refresh", headers=headers)
    assert resp.status_code == 200
    json = resp.get_json()
    assert "access_token" in json
