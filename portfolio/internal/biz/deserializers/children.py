from typing import List, Optional

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.parents import ParentsDeserializer, DES_FROM_DB_INFO_PARENTS
from portfolio.models.account_main import AccountMain
from portfolio.models.children import Children
from portfolio.models.parents import Parents

DES_FOR_ADD_CHILD = 'des-for-add-child'
DES_FROM_DB_INFO_CHILD = 'des-from-db-info-child'
DES_FROM_DB_ALL_CHILDREN = 'des-from-db-all-children'
DES_FROM_DB_INFO_CHILDREN = 'des-from-db-info-children'
DES_FROM_DB_INFO_CHILD_WITH_PARENTS = 'des-from-db-info-child-with-parents'
DES_FROM_DB_INFO_DETAIL_CHILD = 'des-from-db-info-detail-child'


class ChildrenDeserialize(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FOR_ADD_CHILD:
            return cls._des_for_add_child
        elif format_des == DES_FROM_DB_INFO_CHILD:
            return cls._des_from_db_info_child
        elif format_des == DES_FROM_DB_ALL_CHILDREN:
            return cls._des_from_db_all_children
        elif format_des == DES_FROM_DB_INFO_CHILDREN:
            return cls._des_from_db_info_children
        elif format_des == DES_FROM_DB_INFO_CHILD_WITH_PARENTS:
            return cls._des_from_db_info_child_with_parents
        elif format_des == DES_FROM_DB_INFO_DETAIL_CHILD:
            return cls._des_from_db_info_detail_child
        else:
            raise TypeError

    @staticmethod
    def _des_for_add_child(child_dict) -> Children:
        return Children(
            name=child_dict.get('name'),
            surname=child_dict.get('surname'),
            date_born=child_dict.get('date_born')
        )

    @staticmethod
    def _des_from_db_info_child(child_parents_dict) -> Children:
        return Children(
            id=child_parents_dict['id'],
            name=child_parents_dict['children_name'],
            surname=child_parents_dict['children_surname'],
            date_born=child_parents_dict['children_date_born'],
            parents=ParentsDeserializer.deserialize(child_parents_dict, DES_FROM_DB_INFO_PARENTS)
        )

    @staticmethod
    def _des_from_db_all_children(list_children) -> List[Children]:
        return [
            Children(
                id=list_children[i]['children_id'],
                name=list_children[i]['children_name'],
                surname=list_children[i]['children_surname'],
                date_born=list_children[i]['children_date_born'],
                parents=Parents(
                    id=list_children[i]['children_']
                )
            )
            for i in range(len(list_children))
        ]

    @staticmethod
    def _des_from_db_info_children(child_dict) -> Children:
        return Children(
            id=child_dict['children_id'],
            name=child_dict['children_name'],
            surname=child_dict['children_surname'],
            date_born=child_dict.get('children_date_born')
        )

    @staticmethod
    def _des_from_db_info_child_with_parents(row_dict) -> Children:
        return Children(
            id=row_dict['children_id'],
            name=row_dict['children_name'],
            surname=row_dict['children_surname'],
            date_born=row_dict['children_date_born'],
            parents=Parents(
                id=row_dict['children_parents_id'],
                account_main=AccountMain(
                    id=row_dict['parents_account_main_id']
                )
            )
        )

    @staticmethod
    def _des_from_db_info_detail_child(row_dict) -> Children:
        return Children(
            id=row_dict['children_id'],
            name=row_dict['children_name'],
            surname=row_dict['children_surname'],
            date_born=row_dict['children_date_born'],
            parents=Parents(
                id=row_dict['children_parents_id']
            )
        )
