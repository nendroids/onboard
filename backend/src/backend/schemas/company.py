# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: companies                                                                               │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields, validate


class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    industry = fields.Str(validate=validate.Length(max=100), allow_none=True)
    website = fields.Url(allow_none=True)
    description = fields.Str(allow_none=True)
    company_size = fields.Str(validate=validate.Length(max=50), allow_none=True)
    established_year = fields.Int(
        validate=validate.Range(min=1800, max=2030), allow_none=True
    )
    location = fields.Str(validate=validate.Length(max=150), allow_none=True)
    logo_path = fields.Str(dump_only=True)
    hr_name = fields.Str(validate=validate.Length(max=150), allow_none=True)
    hr_email = fields.Email(allow_none=True)
    hr_phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    rejection_reason = fields.Str(dump_only=True)
    approved_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_approved = fields.Bool(dump_only=True)
    active_jobs_count = fields.Int(dump_only=True)
    total_applicants = fields.Int(dump_only=True)
    user = fields.Nested(
        "UserSchema",
        dump_only=True,
        exclude=("company_profile", "student_profile", "password"),
    )


class CompanyUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=150))
    industry = fields.Str(validate=validate.Length(max=100), allow_none=True)
    website = fields.Url(allow_none=True)
    description = fields.Str(allow_none=True)
    company_size = fields.Str(validate=validate.Length(max=50), allow_none=True)
    established_year = fields.Int(
        validate=validate.Range(min=1800, max=2030), allow_none=True
    )
    location = fields.Str(validate=validate.Length(max=150), allow_none=True)
    hr_name = fields.Str(validate=validate.Length(max=150), allow_none=True)
    hr_email = fields.Email(allow_none=True)
    hr_phone = fields.Str(validate=validate.Length(max=20), allow_none=True)


class CompanyApprovalSchema(Schema):
    action = fields.Str(required=True, validate=validate.OneOf(["approve", "reject"]))
    rejection_reason = fields.Str(allow_none=True)
