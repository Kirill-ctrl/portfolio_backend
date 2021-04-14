from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.children import Children

DES_FOR_ADD_CHILD = 'des-for-add-child'

class ChildrenDeserialize(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FOR_ADD_CHILD:
            return cls._des_for_add_child
        else:
            raise TypeError

    @staticmethod
    def _des_for_add_child(child_dict) -> Children:
        return Children(
            name=child_dict.get('name'),
            surname=child_dict.get('surname'),
            date_born=child_dict.get('date_born')
        )
