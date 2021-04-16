from flask import request, json

from portfolio.internal.biz.services.events import EventsService
from portfolio.internal.biz.services.organisation import OrganisationService


def get_query_params_search_organisation(func):
    def wrapper(*args, **kwargs):
        if not request.args.get('organisation_name'):
            response = func(*args, organisation_id=None, **kwargs)
            return response
        organisation_name = request.args.get('organisation_name')

        organisation, err = OrganisationService.get_id_by_organisation_name(organisation_name)
        if err:
            return json.dumps(err)

        response = func(*args, organisation_id=organisation.id)
        return response

    wrapper.__name__ = func.__name__
    return wrapper


def get_query_params_search_event(func):
    def wrapper(*args, **kwargs):
        if not request.args.get('events_name'):
            response = func(*args, events_id=None, **kwargs)
            return response
        events_name = request.args.get('events_name')

        events, err = EventsService.get_id_by_events_name(events_name)
        if err:
            return json.dumps(err)

        response = func(*args, events_id=events.id, **kwargs)
        return response

    wrapper.__name__ = func.__name__
    return wrapper
