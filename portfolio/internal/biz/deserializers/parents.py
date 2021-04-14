from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.parents import Parents

DES_FROM_ADD_PARENTS = 'des-from-add-parents'
DES_FROM_EDIT_PARENTS = 'des-from-edit-parents'


class ParentsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_ADD_PARENTS:
            return cls._deserializer_from_add_parents
        else:
            raise TypeError

    @staticmethod
    def _deserializer_from_add_parents(parents_dict):
        return Parents(
            name=parents_dict.get('name'),
            surname=parents_dict.get('surname')
        )

    @staticmethod
    def _deserializer_from_edit_parents(parents_dict):
        return Parents(
            name=parents_dict.get('name') if parents_dict.get('name') else '-1',
            surname=parents_dict.get('surname') if parents_dict.get('surname') else '-1'
        )
