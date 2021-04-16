from typing import List

from portfolio.models.events_child import EventsChild


def get_count_hours_in_events(list_events_child: List[EventsChild]):
    count_hours = 0
    for event in list_events_child:
        count_hours += event.events.hours
    return count_hours
