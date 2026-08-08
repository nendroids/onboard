# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: placements                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields


class PlacementSchema(Schema):
    id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    offered_salary = fields.Str(allow_none=True)
    ctc_offered = fields.Str(allow_none=True)
    offer_letter_path = fields.Str(dump_only=True)
    joining_date = fields.DateTime(allow_none=True)
    placed_on = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    job = fields.Nested("JobSchema", dump_only=True, only=("id", "title", "company"))
    student = fields.Nested(
        "StudentSchema", dump_only=True, only=("id", "full_name", "student_id")
    )
    company = fields.Nested("CompanySchema", dump_only=True, only=("id", "name"))
