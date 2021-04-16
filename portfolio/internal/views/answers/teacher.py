from typing import List

from portfolio.internal.biz.serializers.organisation import OrganisationSerializer, SER_FOR_DETAIL_TEACHER_ORGANISATION
from portfolio.internal.biz.serializers.teacher import TeacherSerializer, SER_FOR_ADD_TEACHER, SER_FOR_EDIT_TEACHER, \
    SER_FOR_DELETE_TEACHER
from portfolio.models.teacher import Teacher


def get_response_add_teacher(teacher: Teacher):
    return TeacherSerializer.serialize(teacher, SER_FOR_ADD_TEACHER)


def get_response_edit_teacher(teacher: Teacher):
    return TeacherSerializer.serialize(teacher, SER_FOR_EDIT_TEACHER)


def get_response_delete_teacher(teacher: Teacher):
    return TeacherSerializer.serialize(teacher, SER_FOR_DELETE_TEACHER)


def get_response_detail_organisation(list_teacher_organisation: List[Teacher]):
    return OrganisationSerializer.serialize(list_teacher_organisation, SER_FOR_DETAIL_TEACHER_ORGANISATION)