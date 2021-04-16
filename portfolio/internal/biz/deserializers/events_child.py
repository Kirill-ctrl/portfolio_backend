from typing import List

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.children_organisation import ChildrenOrganisationDeserializer, \
    DES_FROM_DB_GET_DETAIL_LEARNER
from portfolio.internal.biz.deserializers.events import EventDeserializer, DES_FROM_DB_INFO_CHILD_EVENTS
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events_child import EventsChild

DES_FROM_DB_GET_INFO_CHILD_ORGANISATION = 'des-from-db-info-child-organisation'


class EventsChildDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_INFO_CHILD_ORGANISATION:
            return cls._des_from_db_get_info_child_organisation
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_info_child_organisation(data) -> List[EventsChild]:
        return [
            EventsChild(
                id=data[i]['events_child_id'],
                status=data[i]['events_child_status'],
                events=EventDeserializer.deserialize(data[i], DES_FROM_DB_INFO_CHILD_EVENTS),
                children_organisation=ChildrenOrganisationDeserializer.deserialize(data[i], DES_FROM_DB_GET_DETAIL_LEARNER)
            )
            for i in range(len(data))
        ]
