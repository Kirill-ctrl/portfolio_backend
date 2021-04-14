from marshmallow import Schema, fields


class RecoveryPasswordSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Обязательное поле'})
    email = fields.Email(required=True, error_messages={'required': 'Обязательное поле'})
