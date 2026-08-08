# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: students                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields, validate


class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    student_id = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    education = fields.Str(validate=validate.Length(max=255), allow_none=True)
    branch = fields.Str(validate=validate.Length(max=100), allow_none=True)
    cgpa = fields.Float(validate=validate.Range(min=0.0, max=10.0), allow_none=True)
    graduation_year = fields.Int(
        validate=validate.Range(min=2000, max=2035), allow_none=True
    )
    skills = fields.Str(validate=validate.Length(max=500), allow_none=True)
    certifications = fields.Str(allow_none=True)
    resume_path = fields.Str(dump_only=True)
    headline = fields.Str(validate=validate.Length(max=200), allow_none=True)
    about_me = fields.Str(allow_none=True)
    experience = fields.Str(allow_none=True)
    preferred_roles = fields.Str(validate=validate.Length(max=255), allow_none=True)
    github_url = fields.Url(allow_none=True)
    linkedin_url = fields.Url(allow_none=True)
    portfolio_url = fields.Url(allow_none=True)
    placement_status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    skills_list = fields.List(fields.Str(), dump_only=True)
    is_placed = fields.Bool(dump_only=True)
    active_applications_count = fields.Int(dump_only=True)
    user = fields.Nested(
        "UserSchema",
        dump_only=True,
        exclude=("student_profile", "company_profile", "password"),
    )


class StudentUpdateSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=2, max=150))
    phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    education = fields.Str(validate=validate.Length(max=255), allow_none=True)
    branch = fields.Str(validate=validate.Length(max=100), allow_none=True)
    cgpa = fields.Float(validate=validate.Range(min=0.0, max=10.0), allow_none=True)
    graduation_year = fields.Int(
        validate=validate.Range(min=2000, max=2035), allow_none=True
    )
    skills = fields.Str(validate=validate.Length(max=500), allow_none=True)
    certifications = fields.Str(allow_none=True)
    headline = fields.Str(validate=validate.Length(max=200), allow_none=True)
    about_me = fields.Str(allow_none=True)
    experience = fields.Str(allow_none=True)
    preferred_roles = fields.Str(validate=validate.Length(max=255), allow_none=True)
    github_url = fields.Url(allow_none=True)
    linkedin_url = fields.Url(allow_none=True)
    portfolio_url = fields.Url(allow_none=True)
