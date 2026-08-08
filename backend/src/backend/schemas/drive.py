# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: drives                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields, validate


class JobSchema(Schema):

    id = fields.Int(dump_only=True)
    company_id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    description = fields.Str(required=True)
    skills_required = fields.Str(validate=validate.Length(max=500), allow_none=True)
    eligibility_criteria = fields.Str(allow_none=True)
    min_cgpa = fields.Float(validate=validate.Range(min=0.0, max=10.0), allow_none=True)
    eligible_branches = fields.Str(validate=validate.Length(max=300), allow_none=True)
    eligible_year = fields.Int(validate=validate.Range(min=1, max=5), allow_none=True)
    experience_required = fields.Str(validate=validate.Length(max=100), allow_none=True)
    employment_type = fields.Str(validate=validate.Length(max=50), allow_none=True)
    location = fields.Str(validate=validate.Length(max=150), allow_none=True)
    openings = fields.Int(load_default=1, validate=validate.Range(min=1))
    salary_range = fields.Str(validate=validate.Length(max=100), allow_none=True)
    package_lpa = fields.Float(validate=validate.Range(min=0.0), allow_none=True)
    bond_period = fields.Str(validate=validate.Length(max=50), allow_none=True)
    status = fields.Str(dump_only=True)
    rejection_reason = fields.Str(dump_only=True)
    approved_at = fields.DateTime(dump_only=True)
    deadline = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_open = fields.Bool(dump_only=True)
    is_deadline_passed = fields.Bool(dump_only=True)
    applicant_count = fields.Int(dump_only=True)
    shortlisted_count = fields.Int(dump_only=True)
    selected_count = fields.Int(dump_only=True)
    skills_list = fields.List(fields.Str(), dump_only=True)
    summary_text = fields.Str(dump_only=True)
    company = fields.Nested(
        "CompanySchema",
        dump_only=True,
        only=("id", "name", "industry", "location", "logo_path"),
    )


class JobCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    description = fields.Str(required=True)
    skills_required = fields.Str(validate=validate.Length(max=500), allow_none=True)
    eligibility_criteria = fields.Str(allow_none=True)
    min_cgpa = fields.Float(validate=validate.Range(min=0.0, max=10.0), allow_none=True)
    eligible_branches = fields.Str(validate=validate.Length(max=300), allow_none=True)
    eligible_year = fields.Int(validate=validate.Range(min=1, max=5), allow_none=True)
    experience_required = fields.Str(validate=validate.Length(max=100), allow_none=True)
    employment_type = fields.Str(validate=validate.Length(max=50), allow_none=True)
    location = fields.Str(validate=validate.Length(max=150), allow_none=True)
    openings = fields.Int(load_default=1, validate=validate.Range(min=1))
    salary_range = fields.Str(validate=validate.Length(max=100), allow_none=True)
    package_lpa = fields.Float(validate=validate.Range(min=0.0), allow_none=True)
    bond_period = fields.Str(validate=validate.Length(max=50), allow_none=True)
    deadline = fields.DateTime(allow_none=True)


class JobUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=2, max=150))
    description = fields.Str()
    skills_required = fields.Str(validate=validate.Length(max=500), allow_none=True)
    eligibility_criteria = fields.Str(allow_none=True)
    min_cgpa = fields.Float(validate=validate.Range(min=0.0, max=10.0), allow_none=True)
    eligible_branches = fields.Str(validate=validate.Length(max=300), allow_none=True)
    eligible_year = fields.Int(validate=validate.Range(min=1, max=5), allow_none=True)
    experience_required = fields.Str(validate=validate.Length(max=100), allow_none=True)
    employment_type = fields.Str(validate=validate.Length(max=50), allow_none=True)
    location = fields.Str(validate=validate.Length(max=150), allow_none=True)
    openings = fields.Int(validate=validate.Range(min=1))
    salary_range = fields.Str(validate=validate.Length(max=100), allow_none=True)
    package_lpa = fields.Float(validate=validate.Range(min=0.0), allow_none=True)
    bond_period = fields.Str(validate=validate.Length(max=50), allow_none=True)
    deadline = fields.DateTime(allow_none=True)


class JobApprovalSchema(Schema):
    action = fields.Str(required=True, validate=validate.OneOf(["approve", "reject"]))
    rejection_reason = fields.Str(allow_none=True)


class DriveSchema(Schema):
    id = fields.Int(dump_only=True)
    company_id = fields.Int(required=True)
    job_title = fields.Str(required=True, validate=validate.Length(max=100))
    job_description = fields.Str(required=True)
    eligible_branches = fields.Str(required=True, validate=validate.Length(max=200))
    min_cgpa = fields.Float(required=True)
    eligible_year = fields.Int(required=True)
    package_lpa = fields.Float(required=True)
    application_deadline = fields.DateTime(required=True)
    status = fields.Str(dump_only=True)
    rejection_reason = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
