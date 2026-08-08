"""
Pytest configuration and shared fixtures for the Onboard backend tests.
"""

import pytest
from datetime import datetime, timedelta
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
import uuid

from backend import create_app
from backend.extensions import db as _db
from backend.config.testing import TestingConfig
from backend.models import User, Student, Company, Job, Application


@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask app for testing."""
    app = create_app(TestingConfig)
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app: Flask):
    """Provide a database session and rollback after each test."""
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Return a test client."""
    return app.test_client()


@pytest.fixture
def admin_user(db) -> User:
    """Create and return an admin user."""
    suffix = uuid.uuid4().hex[:8]
    user = User(
        username="admin",
        email="admin@example.com",
        role="admin",
        status="approved",
    )
    user.set_password("adminpass")
    db.session.add(user)
    db.session.flush()  # flush, not commit
    return user


@pytest.fixture
def company_user(db) -> User:
    """Create a company user with a Company profile (approved)."""
    suffix = uuid.uuid4().hex[:8]
    user = User(
        username="company",
        email="company@example.com",
        role="company",
        status="approved",
    )
    user.set_password("companypass")
    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        name="Test Corp",
        industry="Tech",
        approved_at=db.func.now(),
    )
    db.session.add(company)
    db.session.flush()
    return user


@pytest.fixture
def student_user(db) -> User:
    """Create a student user with a Student profile."""
    suffix = uuid.uuid4().hex[:8]
    user = User(
        username="student",
        email="student@example.com",
        role="student",
        status="approved",
    )
    user.set_password("studentpass")
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        full_name="Test Student",
        student_id="STU123",
        branch="CSE",
        cgpa=8.5,
        graduation_year=2025,
    )
    db.session.add(student)
    db.session.flush()
    return user


@pytest.fixture
def admin_token(admin_user: User) -> str:
    """Return a valid JWT access token for admin."""
    return create_access_token(
        identity=str(admin_user.id),
        additional_claims={"role": admin_user.role, "status": admin_user.status},
    )


@pytest.fixture
def company_token(company_user: User) -> str:
    """Return a valid JWT access token for company."""
    return create_access_token(
        identity=str(company_user.id),
        additional_claims={"role": company_user.role, "status": company_user.status},
    )


@pytest.fixture
def student_token(student_user: User) -> str:
    """Return a valid JWT access token for student."""
    return create_access_token(
        identity=str(student_user.id),
        additional_claims={"role": student_user.role, "status": student_user.status},
    )


@pytest.fixture
def auth_headers(admin_token: str) -> dict:
    """Return Authorization headers with Bearer token."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def company_auth_headers(company_token: str) -> dict:
    return {"Authorization": f"Bearer {company_token}"}


@pytest.fixture
def student_auth_headers(student_token: str) -> dict:
    return {"Authorization": f"Bearer {student_token}"}


@pytest.fixture
def approved_job(company_user: User, db) -> Job:
    """Create an approved job for the test company."""
    company = company_user.company_profile
    job = Job(
        company_id=company.id,
        title="Software Engineer",
        description="Develop software",
        status="approved",
        approved_at=db.func.now(),
        deadline=datetime.utcnow() + timedelta(days=30),  # SQLite compatible
    )
    db.session.add(job)
    db.session.flush()
    return job


@pytest.fixture
def pending_job(company_user: User, db) -> Job:
    """Create a pending job for the test company."""
    company = company_user.company_profile
    job = Job(
        company_id=company.id,
        title="Data Analyst",
        description="Analyze data",
        status="pending",
    )
    db.session.add(job)
    db.session.flush()
    return job


@pytest.fixture
def application(student_user: User, approved_job: Job, db) -> Application:
    """Create an application for the student to the approved job."""
    app = Application(
        student_id=student_user.student_profile.id,
        job_id=approved_job.id,
        status="applied",
    )
    db.session.add(app)
    db.session.flush()
    return app
