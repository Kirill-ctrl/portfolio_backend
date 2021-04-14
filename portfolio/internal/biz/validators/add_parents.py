from marshmallow import Schema, fields


class AddParentsSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Обязательное поле'})
    surname = fields.Str(required=True, error_messages={'required': 'Обязательно поле'})
