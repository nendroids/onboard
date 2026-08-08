# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: common                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields


class PaginationSchema(Schema):
    page = fields.Int(load_default=1)
    per_page = fields.Int(load_default=20)


class ErrorSchema(Schema):
    error = fields.Str(required=True)
    message = fields.Str()
