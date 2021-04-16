from marshmallow import Schema, fields


class AddAchievementSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    point = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    nomination = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
