# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: interviews                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields, validate

VALID_INTERVIEW_STATUSES = ["scheduled", "completed", "cancelled", "rescheduled"]


class InterviewSchema(Schema):
    id = fields.Int(dump_only=True)
    application_id = fields.Int(required=True)
    scheduled_at = fields.DateTime(required=True)
    mode = fields.Str(validate=validate.Length(max=50), allow_none=True)
    link = fields.Url(allow_none=True)
    location = fields.Str(validate=validate.Length(max=255), allow_none=True)
    feedback = fields.Str(allow_none=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    application = fields.Nested(
        "ApplicationSchema",
        dump_only=True,
        only=("id", "student", "job"),
    )


class InterviewCreateSchema(Schema):
    scheduled_at = fields.DateTime(required=True)
    mode = fields.Str(validate=validate.Length(max=50), allow_none=True)
    link = fields.Url(allow_none=True)
    location = fields.Str(validate=validate.Length(max=255), allow_none=True)


class InterviewUpdateSchema(Schema):
    status = fields.Str(validate=validate.OneOf(VALID_INTERVIEW_STATUSES))
    feedback = fields.Str(allow_none=True)
    scheduled_at = fields.DateTime(allow_none=True)
    mode = fields.Str(validate=validate.Length(max=50), allow_none=True)
    link = fields.Url(allow_none=True)
    location = fields.Str(validate=validate.Length(max=255), allow_none=True)
