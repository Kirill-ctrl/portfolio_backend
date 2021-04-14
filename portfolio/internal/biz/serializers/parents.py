from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.parents import Parents

SER_FOR_ADD_PARENTS = 'ser-for-add-parents'
SER_FOR_EDIT_PARENTS = 'ser-for-edit-parents'


class ParentsSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_PARENTS:
            return cls._ser_for_add_parents
        elif format_ser == SER_FOR_EDIT_PARENTS:
            return cls._ser_for_edit_parents
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_parents(parents: Parents):
        return {
            'id': parents.id,
            'created_at': parents.created_at,
            'edited_at': parents.edited_at,
            'name': parents.name,
            'surname': parents.surname,
            'account_main_id': parents.account_main.id
        }

    @staticmethod
    def _ser_for_edit_parents(parents: Parents):
        return {
            'id': parents.id,
            'edited_at': parents.edited_at,
            'name': parents.name,
            'surname': parents.surname,
            'account_main_id': parents.account_main.id
        }
