"""
Unit tests for model classes: relationships, properties, and methods.
"""

import pytest
from datetime import datetime, timezone
from backend.models import User, Student, Company, Job, Application, Placement
from backend.extensions import db


def test_user_password_hashing(db):
    user = User(username="test", email="test@example.com", role="student")
    user.set_password("secret")
    db.session.add(user)
    db.session.commit()

    assert user.check_password("secret") is True
    assert user.check_password("wrong") is False
    assert user.password_hash != "secret"


def test_student_properties(student_user):
    student = student_user.student_profile
    assert student.skills_list == []  # default empty
    assert student.is_placed is False
    assert student.active_applications_count == 0


def test_company_approval(company_user):
    company = company_user.company_profile
    assert company.is_approved is True  # created with approved_at
    assert company.active_jobs_count == 0


def test_job_properties(approved_job):
    job = approved_job
    assert job.is_open is True
    assert job.is_deadline_passed is False
    assert job.applicant_count == 0
    assert job.skills_list == []
    assert job.summary_text == "Develop software"


def test_application_status_update(application):
    assert application.status == "applied"
    application.update_status("shortlisted", feedback="Good fit")
    assert application.status == "shortlisted"
    assert application.feedback == "Good fit"
    assert application.is_active is True


def test_placement_creation(application, db):
    # Create a placement from the application
    placement = Placement(
        job_id=application.job_id,
        student_id=application.student_id,
        offered_salary="10 LPA",
        ctc_offered="12 LPA",
    )
    db.session.add(placement)
    db.session.commit()
    assert placement.company is not None
    assert placement.id is not None


def test_user_relationships(db, student_user, company_user):
    # Check relationships
    assert student_user.student_profile is not None
    assert company_user.company_profile is not None
    assert student_user.student_profile.user == student_user
    assert company_user.company_profile.user == company_user


def test_soft_delete_mixin(application, db):
    application.soft_delete()
    db.session.commit()
    assert application.is_deleted is True
    assert application.deleted_at is not None
