from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.teacher import TeacherSerializer, SER_FOR_DETAIL_TEACHER
from portfolio.models.organisation import Organisation
from portfolio.models.teacher import Teacher

SER_FOR_ADD_ORGANISATION = 'ser-for-add-organisation'
SER_FOR_EDIT_ORGANISATION = 'ser-for-edit-organisation'
SER_FOR_DELETE_ORGANISATION = 'ser-for-delete-organisation'
SER_FOR_DETAIL_TEACHER_ORGANISATION = 'ser-for-detail-teacher-organisation'
SER_FOR_GET_LIST_ORGANISATION = 'ser-for-get-list-organisation'
SER_FOR_GET_DETAIL_ORGANISATION = 'ser-for-get-detail-organisation'


class OrganisationSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_ORGANISATION:
            return cls._ser_for_add_organisation
        elif format_ser == SER_FOR_EDIT_ORGANISATION:
            return cls._ser_for_edit_organisation
        elif format_ser == SER_FOR_DELETE_ORGANISATION:
            return cls._ser_for_delete_organisation
        elif format_ser == SER_FOR_DETAIL_TEACHER_ORGANISATION:
            return cls._ser_for_detail_teacher_organisation
        elif format_ser == SER_FOR_GET_LIST_ORGANISATION:
            return cls._ser_for_get_list_organisation
        elif format_ser == SER_FOR_GET_DETAIL_ORGANISATION:
            return cls._ser_for_get_detail_organisation
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_organisation(organisation: Organisation):
        return {
            'id': organisation.id,
            'created_at': organisation.created_at,
            'edited_at': organisation.edited_at,
            'name': organisation.name,
            'login': organisation.login,
            'photo_link': organisation.photo_link,
            'description': organisation.description,
            'account_main': organisation.account_main.id
        }

    @staticmethod
    def _ser_for_edit_organisation(organisation: Organisation):
        return {
            'id': organisation.id,
            'edited_at': organisation.edited_at,
            'name': organisation.name,
            'login': organisation.login,
            'photo_link': organisation.photo_link,
            'description': organisation.description,
            'account_main_id': organisation.account_main.id
        }

    @staticmethod
    def _ser_for_delete_organisation(organisation: Organisation):
        return {
            'id': organisation.id
        }

    @staticmethod
    def _ser_for_detail_teacher_organisation(list_teacher_organisation: List[Teacher]):
        return {
            'organisation_id': list_teacher_organisation[0].organisation.id,
            'organisation_created_at': list_teacher_organisation[0].organisation.created_at,
            'organisation_name': list_teacher_organisation[0].organisation.name,
            'organisation_photo_link': list_teacher_organisation[0].organisation.photo_link,
            'organisation_description': list_teacher_organisation[0].organisation.description,
            'teachers': [
                TeacherSerializer.serialize(list_teacher_organisation[i], SER_FOR_DETAIL_TEACHER)
                for i in range(len(list_teacher_organisation))
            ]
        }

    @staticmethod
    def _ser_for_get_list_organisation(list_organisations: List[Organisation]):
        return {
            'organisation': {
                'id': list_organisations[i].id,
                'name': list_organisations[i].name,
                'login': list_organisations[i].login,
                'photo_link': list_organisations[i].photo_link,
                'description': list_organisations[i].description
            }
            for i in range(len(list_organisations))
        }

    @staticmethod
    def _ser_for_get_detail_organisation(organisation: Organisation):
        return {
            'id': organisation.id,
            'name': organisation.name,
            'login': organisation.login,
            'photo_link': organisation.photo_link,
            'description': organisation.description
        }