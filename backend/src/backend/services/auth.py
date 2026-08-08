# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ services: auth                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from backend.extensions import db
from backend.models import User, Student, Company, AuditLog


class AuthService:
    """Authentication & registration service (JWT)."""

    @staticmethod
    def register_student(data: dict[str, Any]) -> dict[str, Any]:
        """
        Register a new student.
        Required keys: username, email, password, full_name, student_id
        Optional: phone, branch, cgpa, graduation_year, skills, ...
        """
        if User.query.filter(
            (User.email == data["email"]) | (User.username == data["username"])
        ).first():
            raise ValueError("Email or username already registered")

        if Student.query.filter_by(student_id=data["student_id"]).first():
            raise ValueError("Student ID already exists")

        user = User(
            username=data["username"],
            email=data["email"],
            role="student",
            status="approved",  # students are auto-approved
        )
        user.set_password(data["password"])

        student = Student(
            user=user,
            full_name=data["full_name"],
            student_id=data["student_id"],
            phone=data.get("phone"),
            education=data.get("education"),
            branch=data.get("branch"),
            cgpa=data.get("cgpa"),
            graduation_year=data.get("graduation_year"),
            skills=data.get("skills"),
            certifications=data.get("certifications"),
            headline=data.get("headline"),
            about_me=data.get("about_me"),
            experience=data.get("experience"),
            preferred_roles=data.get("preferred_roles"),
            github_url=data.get("github_url"),
            linkedin_url=data.get("linkedin_url"),
            portfolio_url=data.get("portfolio_url"),
        )

        try:
            db.session.add(user)
            db.session.add(student)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Registration failed due to data conflict")

        AuditLog.log(
            action="student_registered",
            user_id=user.id,
            entity_type="student",
            entity_id=student.id,
        )
        db.session.commit()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role, "status": user.status},
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "student_id": student.id,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            },
            "message": "Student registered successfully",
        }

    @staticmethod
    def register_company(data: dict[str, Any]) -> dict[str, Any]:
        """
        Register a new company (status = pending until admin approval).
        Required: username, email, password, name
        """
        if User.query.filter(
            (User.email == data["email"]) | (User.username == data["username"])
        ).first():
            raise ValueError("Email or username already registered")

        user = User(
            username=data["username"],
            email=data["email"],
            role="company",
            status="pending",
        )
        user.set_password(data["password"])

        company = Company(
            user=user,
            name=data["name"],
            industry=data.get("industry"),
            website=data.get("website"),
            description=data.get("description"),
            company_size=data.get("company_size"),
            established_year=data.get("established_year"),
            location=data.get("location"),
            hr_name=data.get("hr_name"),
            hr_email=data.get("hr_email"),
            hr_phone=data.get("hr_phone"),
        )

        try:
            db.session.add(user)
            db.session.add(company)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Registration failed due to data conflict")

        AuditLog.log(
            action="company_registered",
            user_id=user.id,
            entity_type="company",
            entity_id=company.id,
        )
        db.session.commit()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role, "status": user.status},
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "company_id": company.id,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            },
            "message": "Company registered. Awaiting admin approval.",
        }

    @staticmethod
    def login(email: str, password: str) -> dict[str, Any]:
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ValueError("Invalid email or password")

        if user.is_blacklisted:
            raise ValueError("Account is blacklisted")

        if user.role != "admin" and user.status != "approved":
            raise ValueError(f"Account is {user.status}. Contact admin.")

        user.record_login()
        db.session.commit()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role, "status": user.status},
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        AuditLog.log(action="user_login", user_id=user.id)
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            },
        }
