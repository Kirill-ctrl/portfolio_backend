from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.events_child import EventsChild

SER_FOR_ADD_ACTIVITY = 'ser-for-add-activity'


class EventsChildSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_ACTIVITY:
            return cls._ser_for_add_activity
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
