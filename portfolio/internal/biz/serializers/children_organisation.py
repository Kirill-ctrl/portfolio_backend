from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.children import ChildrenSerializer
from portfolio.models.children_organisation import ChildrenOrganisation

SER_FOR_GET_LIST_LEARNERS = 'ser-for-get-list-learners'


class ChildrenOrganisationSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_GET_LIST_LEARNERS:
            return cls._ser_for_get_list_learners
        else:
            raise TypeError

    @staticmethod
    def _ser_for_get_list_learners(list_learners: List[ChildrenOrganisation]):
        return {
            'children': {
                'id': list_learners[i].id,
                'teacher': {
                    'id': list_learners[i].teacher.id,
                },
                'children': ChildrenSerializer.serialize
            }
            for i in range(len(list_learners))
        }
