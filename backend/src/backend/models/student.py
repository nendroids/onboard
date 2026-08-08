# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ models: student                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from backend.extensions import db
from backend.models import Application, BaseModel


class Student(BaseModel):

    __tablename__ = "students"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    full_name = db.Column(db.String(150), nullable=False, index=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    branch = db.Column(db.String(100), nullable=True, index=True)
    cgpa = db.Column(db.Float, nullable=True, index=True)
    graduation_year = db.Column(db.Integer, nullable=True, index=True)
    skills = db.Column(db.String(500), nullable=True)  # comma-separated
    certifications = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)
    headline = db.Column(db.String(200), nullable=True)
    about_me = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    preferred_roles = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)

    placement_status = db.Column(
        db.String(20), default="not_placed", nullable=False, index=True
    )

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship(
        "Application",
        back_populates="student",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    placements = db.relationship(
        "Placement",
        back_populates="student",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    export = db.relationship(
        "ExportJob",
        back_populates="student",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @property
    def skills_list(self) -> list[str]:
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    @property
    def is_placed(self) -> bool:
        return self.placement_status == "placed"

    @property
    def active_applications_count(self) -> int:
        return self.applications.filter(
            Application.status.notin_(["selected", "rejected"])
        ).count()

    def mark_placed(self) -> None:
        self.placement_status = "placed"

    def __repr__(self) -> str:
        return f"<Student {self.full_name!r} [{self.student_id}]>"
