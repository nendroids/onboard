# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: users                                                                                   │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import (
    INCLUDE,
    Schema,
    fields,
    validate,
)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=6)
    )
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["admin", "company", "student"]),
    )
    status = fields.Str(dump_only=True)
    is_blacklisted = fields.Bool(dump_only=True)
    blacklist_reason = fields.Str(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    company_profile = fields.Nested("CompanySchema", dump_only=True, exclude=("user",))
    student_profile = fields.Nested("StudentSchema", dump_only=True, exclude=("user",))


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(Schema):
    class Meta:
        unknown = INCLUDE

    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=6)
    )
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["company", "student"]),
    )
