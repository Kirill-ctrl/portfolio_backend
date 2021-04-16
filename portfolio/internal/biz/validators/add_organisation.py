from marshmallow import Schema, fields


class AddOrganisationSchema(Schema):
    name = fields.Str(required=True, allow_none=False, error_messages={'required': 'Это обязательное поле'})
    login = fields.Email(required=True, allow_none=False, error_messages={'required': 'Это обязательное поле'})
    photo_link = fields.Str(required=True, allow_none=False, error_messages={'required': 'Это обязательное поле'})
    description = fields.Str(required=True, allow_none=False, error_messages={'required': 'Это обязательное поле'})
