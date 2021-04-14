from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.parents import ParentsSerializer
from portfolio.models.children import Children

SER_FOR_ADD_CHILD = 'ser-for-add-child'


class ChildrenSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_CHILD:
            return cls._ser_for_add_child
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