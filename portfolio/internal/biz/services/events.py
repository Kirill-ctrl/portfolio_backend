from portfolio.internal.biz.dao.events import EventsDao
from portfolio.models.events import Events


class EventsService:

    @staticmethod
    def add_event(event: Events):
        event, err = EventsDao().add(event)
        if err:
            return None, err
        return event, None

    @staticmethod
    def get_all_events_by_organisation_id(organisation_id: int):
        list_events, err = EventsDao().get_by_organisation_id(organisation_id)
        if err:
            return None, err
        return list_events, None

    @staticmethod
    def get_by_events_id(events_id: int):
        event, err = EventsDao().get_by_id(events_id)
        if err:
            return None, err
        return event, None
