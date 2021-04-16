from typing import List

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FROM_DB_INFO_CHILDREN
from portfolio.internal.biz.deserializers.events import EventDeserializer, DES_FROM_DB_INFO_EVENTS
from portfolio.internal.biz.deserializers.parents import ParentsDeserializer, DES_FROM_DB_INFO_PARENTS
from portfolio.models.children import Children
from portfolio.models.events import Events
from portfolio.models.parents import Parents
from portfolio.models.request_to_organisation import RequestToOrganisation

DES_FROM_DB_GET_LIST_REQUESTS = 'des-from-db-get-list-requests'


class RequestToOrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_LIST_REQUESTS:
            return cls._des_from_db_get_list_requests
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_list_requests(data) -> List[RequestToOrganisation]:
        return [
            RequestToOrganisation(
                id=data[i]['request_id'],
                parents=ParentsDeserializer.deserialize(data[i], DES_FROM_DB_INFO_PARENTS),
                events=EventDeserializer.deserialize(data[i], DES_FROM_DB_INFO_EVENTS),
                children=Children(id=data[i]['request_children_id']),
                status=data[i]['request_status']
            )
            for i in range(len(data))
        ]
