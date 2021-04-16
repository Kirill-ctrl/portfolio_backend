from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.events import Events

SER_FOR_ADD_EVENT = 'ser-for-add-event'
SER_FOR_GET_LIST_EVENTS = 'ser-for-get-list-events'
SER_FOR_GET_DETAIL_EVENT = 'ser-for-get-detail-event'


class EventsSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_EVENT:
            return cls._ser_for_add_event
        elif format_ser == SER_FOR_GET_LIST_EVENTS:
            return cls._ser_for_get_list_events
        elif format_ser == SER_FOR_GET_DETAIL_EVENT:
            return cls._ser_for_get_detail_events
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_event(event: Events):
        return {
            'id': event.id,
            'created_at': event.created_at,
            'edited_at': event.edited_at,
            'type': event.type,
            'name': event.name,
            'date_event': event.date_event,
            'hours': event.hours,
            'skill': event.skill,
            'organisation': {
                'id': event.organisation.id
            }
        }

    @staticmethod
    def _ser_for_get_list_events(list_events: List[Events]):
        return {
            'organisation': {
                'id': list_events[0].organisation.id
            },
            'events': [
                {
                    'id': list_events[i].id,
                    'type': list_events[i].type,
                    'name': list_events[i].name,
                    'date_event': list_events[i].date_event,
                    'hours': list_events[i].hours,
                    'skill': list_events[i].skill
                }
                for i in range(len(list_events))
            ]
        }

    @staticmethod
    def _ser_for_get_detail_events(event: Events):
        return {
            'organisation': {
                'id': event.organisation.id
            },
            'event': {
                'id': event.id,
                'type': event.type,
                'name': event.name,
                'date_event': event.date_event,
                'hours': event.hours,
                'skill': event.skill
            }
        }
