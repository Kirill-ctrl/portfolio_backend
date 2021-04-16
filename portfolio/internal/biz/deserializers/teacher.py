from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.organisation import OrganisationDeserializer, DES_FROM_DB_DETAIL_ORGANISATION
from portfolio.models.teacher import Teacher

DES_FOR_ADD_TEACHER = 'des-for-add-teacher'
DES_FOR_EDIT_TEACHER = 'des-for-edit-teacher'
DES_FROM_DB_DETAIL_TEACHER = 'des-from-db-detail-teacher'


class TeacherDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FOR_ADD_TEACHER:
            return cls._des_for_add_teacher
        elif format_des == DES_FOR_EDIT_TEACHER:
            return cls._des_for_edit_teacher
        elif format_des == DES_FROM_DB_DETAIL_TEACHER:
            return cls._des_from_db_detail_teacher
        else:
            raise TypeError

    @staticmethod
    def _des_for_add_teacher(teacher_dict):
        return Teacher(
            name=teacher_dict.get('name'),
            surname=teacher_dict.get('surname'),
            specialty=teacher_dict.get('specialty')
        )

    @staticmethod
    def _des_for_edit_teacher(teacher_dict):
        return Teacher(
            name=teacher_dict.get('name') if teacher_dict.get('name') else '-1',
            surname=teacher_dict.get('surname') if teacher_dict.get('surname') else '-1',
            specialty=teacher_dict.get('specialty') if teacher_dict.get('specialty') else '-1'
        )

    @staticmethod
    def _des_from_db_detail_teacher(data):
        return [Teacher(
            organisation=OrganisationDeserializer.deserialize(data[0], DES_FROM_DB_DETAIL_ORGANISATION),
            name=data[i]['teacher_name'],
            surname=data[i]['teacher_surname'],
            specialty=data[i]['teacher_specialty']
        ) for i in range(len(data))]
