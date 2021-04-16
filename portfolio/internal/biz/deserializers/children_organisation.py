from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FROM_DB_INFO_CHILDREN, \
    DES_FROM_DB_INFO_DETAIL_CHILD
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.teacher import Teacher

DES_FROM_DB_GET_ALL_LEARNERS = 'des-from-db-get-all-learners'
DES_FROM_DB_GET_DETAIL_LEARNER = 'des-from-db-get-detail-learner'


class ChildrenOrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_ALL_LEARNERS:
            return cls._des_from_db_get_all_learners
        elif format_des == DES_FROM_DB_GET_DETAIL_LEARNER:
            return cls._des_from_db_get_detail_learners
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_all_learners(data):
        return [
            ChildrenOrganisation(
                id=data[i]['children_organisation_id'],
                teacher=Teacher(
                    id=data[i]['children_organisation_teacher_id']
                ),
                children=ChildrenDeserialize.deserialize(data[i], DES_FROM_DB_INFO_CHILDREN)
            )
            for i in range(len(data))
        ]

    @staticmethod
    def _des_from_db_get_detail_learners(row):
        return ChildrenOrganisation(
            id=row['children_organisation_id'],
            children=ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_DETAIL_CHILD)
        )
