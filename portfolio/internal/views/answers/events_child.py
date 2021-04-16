from portfolio.internal.biz.serializers.events_child import EventsChildSerializer, SER_FOR_ADD_ACTIVITY
from portfolio.models.events_child import EventsChild


def get_response_add_activity(events_child: EventsChild):
    return EventsChildSerializer.serialize(events_child, SER_FOR_ADD_ACTIVITY)
