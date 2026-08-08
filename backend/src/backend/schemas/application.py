# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: applications                                                                            │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields, validate


class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)
    cover_letter = fields.Str(allow_none=True)
    feedback = fields.Str(dump_only=True)
    applied_on = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    badge_class = fields.Str(dump_only=True)
    student = fields.Nested(
        "StudentSchema",
        dump_only=True,
        only=(
            "id",
            "full_name",
            "student_id",
            "branch",
            "cgpa",
            "graduation_year",
            "skills",
            "resume_path",
        ),
    )
    job = fields.Nested(
        "JobSchema",
        dump_only=True,
        only=("id", "title", "company", "package_lpa", "deadline", "status"),
    )
    interview = fields.Nested("InterviewSchema", dump_only=True)


class ApplicationCreateSchema(Schema):
    job_id = fields.Int(required=True)
    cover_letter = fields.Str(allow_none=True)


class ApplicationStatusUpdateSchema(Schema):
    status = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["applied", "shortlisted", "interview", "selected", "rejected"]
        ),
    )
    feedback = fields.Str(allow_none=True)
