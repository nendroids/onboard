# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ schemas: notifications                                                                           │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from marshmallow import Schema, fields


class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    message = fields.Str()
    type = fields.Str()
    link = fields.Str(allow_none=True)
    is_read = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    icon_class = fields.Str(dump_only=True)
