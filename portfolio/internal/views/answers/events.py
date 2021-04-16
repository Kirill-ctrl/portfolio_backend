from portfolio.internal.biz.serializers.events import EventsSerializer, SER_FOR_ADD_EVENT
from portfolio.models.events import Events


def get_response_add_event(event: Events):
    return EventsSerializer.serialize(event, SER_FOR_ADD_EVENT)
