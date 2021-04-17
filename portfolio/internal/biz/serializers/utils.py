from typing import List

from flask import json

from portfolio.models.events_child import EventsChild


def get_count_hours_in_events(list_events_child: List[EventsChild]):
    count_hours = 0
    for event in list_events_child:
        count_hours += event.events.hours
    return count_hours


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
