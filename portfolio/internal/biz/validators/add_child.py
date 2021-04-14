from datetime import date

from marshmallow import Schema, fields


def date_validate(value):
    print(value)
    try:
        date.fromisoformat(str(value))
    except:
        raise TypeError("некорректная дата")


class AddChildSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    surname = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_born = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)
