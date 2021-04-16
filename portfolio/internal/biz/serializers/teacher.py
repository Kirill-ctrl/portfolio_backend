from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.teacher import Teacher

SER_FOR_ADD_TEACHER = 'ser-for-add-teacher'
SER_FOR_EDIT_TEACHER = 'ser-for-edit-teacher'
SER_FOR_DELETE_TEACHER = 'ser-for-delete-teacher'
SER_FOR_DETAIL_TEACHER = 'ser-for-detail-teacher'


class TeacherSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_TEACHER:
            return cls._ser_for_add_teacher
        elif format_ser == SER_FOR_EDIT_TEACHER:
            return cls._ser_for_edit_teacher
        elif format_ser == SER_FOR_DELETE_TEACHER:
            return cls._ser_for_delete_teacher
        elif format_ser == SER_FOR_DETAIL_TEACHER:
            return cls._ser_for_detail_teacher
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_teacher(teacher: Teacher):
        return {
            'id': teacher.id,
            'created_at': teacher.created_at,
            'edited_at': teacher.edited_at,
            'name': teacher.name,
            'surname': teacher.surname,
            'specialty': teacher.specialty,
            'organisation': {
                'id': teacher.organisation.id
            }
        }

    @staticmethod
    def _ser_for_edit_teacher(teacher: Teacher):
        return {
            'id': teacher.id,
            'edited_at': teacher.edited_at,
            'name': teacher.name,
            'surname': teacher.surname,
            'specialty': teacher.specialty,
            'organisation': {
                'id': teacher.organisation.id
            }
        }

    @staticmethod
    def _ser_for_delete_teacher(teacher: Teacher):
        return {
            'id': teacher.id
        }

    @staticmethod
    def _ser_for_detail_teacher(teacher: Teacher):
        return {
            'name': teacher.name,
            'surname': teacher.surname,
            'specialty': teacher.specialty
        }
