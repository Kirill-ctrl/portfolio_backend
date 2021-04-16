from marshmallow import Schema, fields

from portfolio.internal.biz.validators.utils import date_validate


class AddTeacherSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    specialty = fields.Str(required=True)


class EditTeacherSchema(Schema):
    name = fields.Str(required=False, allow_none=False)
    surname = fields.Str(required=False, allow_none=False)
    specialty = fields.Str(required=False, allow_none=False)


class AddChildrenSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    surname = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_born = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)


class AddEventSchema(Schema):
    type = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_event = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)
    event_hours = fields.Int(required=True, error_messages={'required': 'Это обязательное поле'})
