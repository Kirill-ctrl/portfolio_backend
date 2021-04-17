from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.events_child import EventsChild

SER_FOR_ADD_ACTIVITY = 'ser-for-add-activity'
SER_FOR_DETAIL_EVENTS_CHILD = 'ser-for-detail-events-child'


class EventsChildSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_ACTIVITY:
            return cls._ser_for_add_activity
        elif format_ser == SER_FOR_DETAIL_EVENTS_CHILD:
            return cls._ser_for_detail_events_child
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_activity(events_child: EventsChild):
        return {
            'id': events_child.id,
            'children_organisation': {
                'id': events_child.children_organisation.id
            },
            'events': {
                'id': events_child.events.id
            },
            'status': events_child.status
        }

    @staticmethod
    def _ser_for_detail_events_child(events_child: EventsChild):
        return {
            'id': events_child.id,
            'status': events_child.status,
            'event': {
                'id': events_child.events.id,
                'type': events_child.events.type,
                'name': events_child.events.name,
                'date_event': events_child.events.date_event,
                'hours': events_child.events.hours,
                'skill': events_child.events.skill
            },
            'children_organisation': {
                events_child.children_organisation.id
            }
        }
