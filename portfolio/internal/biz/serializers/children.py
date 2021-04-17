from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.parents import ParentsSerializer
from portfolio.models.children import Children

SER_FOR_ADD_CHILD = 'ser-for-add-child'
SER_FOR_DETAIL_CHILD = 'ser-for-detail-child'
SER_FOR_GET_LIST_CHILDREN = 'ser-for-get-list-children'
SER_FOR_GET_DETAIL_CHILDREN = 'ser-for-get-detail-children'


class ChildrenSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_CHILD:
            return cls._ser_for_add_child
        elif format_ser == SER_FOR_DETAIL_CHILD:
            return cls._ser_for_detail_child
        elif format_ser == SER_FOR_GET_LIST_CHILDREN:
            return cls._ser_for_get_list_children
        elif format_ser == SER_FOR_GET_DETAIL_CHILDREN:
            return cls._ser_for_get_detail_children
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_child(children: Children):
        return {
            'id': children.id,
            'created_at': children.created_at,
            'edited_at': children.edited_at,
            'name': children.name,
            'surname': children.surname,
            'parents': {
                'id': children.parents.id,
                'account_main': children.parents.account_main.id
            },
        }

    @staticmethod
    def _ser_for_detail_child(children: Children):
        return {
            'id': children.id,
            'name': children.name,
            'surname': children.surname,
            'date_born': children.date_born
        }

    @staticmethod
    def _ser_for_get_list_children(list_children: List[Children]) -> dict:
        return {
            'parents': {
                'id': list_children[0].parents.id
            },
            'children': [
                {
                    'id': list_children[i].id,
                    'name': list_children[i].name,
                    'surname': list_children[i].surname,
                    'date_born': list_children[i].date_born,
                }
                for i in range(len(list_children))
            ]
        }

    @staticmethod
    def _ser_for_get_detail_children(children: Children):
        return {
            'id': children.id,
            'name': children.name,
            'surname': children.surname,
            'date_born': children.date_born,
            'parents': {
                'id': children.parents.id
            }
        }
