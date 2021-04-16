from typing import List

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.events import Events
from portfolio.models.organisation import Organisation

DES_FROM_ADD_EVENT = 'des-from-add-event'
DES_FROM_DB_FULL_EVENTS_BY_ORG_ID = 'des-from-db-full-events-by-org-id'
DES_FROM_DB_GET_DETAIL_EVENT = 'des-from-db-get-detail-event'
DES_FROM_DB_INFO_EVENTS = 'des-from-db-info-events'
DES_FROM_DB_INFO_CHILD_EVENTS = 'des-from-db-info-child-events'


class EventDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_ADD_EVENT:
            return cls._des_from_add_event
        elif format_des == DES_FROM_DB_FULL_EVENTS_BY_ORG_ID:
            return cls._des_from_db_full_events_by_org_id
        elif format_des == DES_FROM_DB_GET_DETAIL_EVENT:
            return cls._des_from_db_get_detail_event
        elif format_des == DES_FROM_DB_INFO_EVENTS:
            return cls._des_from_db_info_events
        elif format_des == DES_FROM_DB_INFO_CHILD_EVENTS:
            return cls._des_from_db_info_child_events
        else:
            raise TypeError

    @staticmethod
    def _des_from_add_event(event_dict) -> Events:
        return Events(
            type=event_dict.get('type'),
            name=event_dict.get('name'),
            date_event=event_dict.get('date_event'),
            hours=event_dict.get('hours'),
            skill=event_dict.get('skill')
        )

    @staticmethod
    def _des_from_db_full_events_by_org_id(list_events) -> List[Events]:
        return [
            Events(
                id=list_events[i]['events_id'],
                type=list_events[i]['events_type'],
                name=list_events[i]['events_name'],
                date_event=list_events[i]['events_date_event'],
                hours=list_events[i]['events_hours'],
                skill=list_events[i]['events_skill'],
                organisation=Organisation(
                    id=list_events[i]['events_organisation_id']
                )
            )
            for i in range(len(list_events))
        ]

    @staticmethod
    def _des_from_db_get_detail_event(event_dict) -> Events:
        return Events(
            id=event_dict['events_id'],
            type=event_dict['events_type'],
            name=event_dict['events_name'],
            date_event=event_dict['events_date_events'],
            hours=event_dict['events_hours'],
            skill=event_dict['events_skill'],
            organisation=Organisation(
                id=event_dict['events_organisation_id'],
            )
        )

    @staticmethod
    def _des_from_db_info_events(event_dict) -> Events:
        return Events(
            id=event_dict['events_id'],
            name=event_dict['events_name'],
            date_event=event_dict['events_date_event'],
            organisation=Organisation(
                id=event_dict['events_organisation_id']
            )
        )

    @staticmethod
    def _des_from_db_info_child_events(row) -> Events:
        return Events(
            id=row['events_id'],
            type=row['events_type'],
            name=row['events_name'],
            date_event=row['events_date_event'],
            hours=row['events_hours'],
            skill=row['events_skill']
        )
