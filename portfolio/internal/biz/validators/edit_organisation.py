from marshmallow import Schema, fields


class EditOrganisationSchema(Schema):
    name = fields.Str(required=False, allow_none=False)
    login = fields.Email(required=False, allow_none=False)
    photo_link = fields.Str(required=False, allow_none=False)
    description = fields.Str(required=False, allow_none=False)
