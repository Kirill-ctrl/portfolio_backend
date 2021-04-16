from marshmallow import Schema, fields

from portfolio.internal.biz.validators.utils import date_validate


class AddChildSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    surname = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_born = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)
