from marshmallow import Schema, fields


class EditParentsSchema(Schema):
    name = fields.Str(required=False, allow_none=False)
    surname = fields.Str(required=False, allow_none=False)
