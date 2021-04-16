from typing import List

from portfolio.internal.biz.serializers.achievements import AchievementsSerializer, SER_FOR_ADD_ACHIEVEMENT
from portfolio.internal.biz.serializers.events import EventsSerializer, SER_FOR_GET_LIST_EVENTS, \
    SER_FOR_GET_DETAIL_EVENT
from portfolio.internal.biz.serializers.organisation import OrganisationSerializer, SER_FOR_GET_LIST_ORGANISATION, \
    SER_FOR_GET_DETAIL_ORGANISATION
from portfolio.internal.biz.serializers.request_to_organisation import RequestToOrganisationSerializer, \
    SER_FOR_MAKE_REQUEST
from portfolio.models.achievements import Achievements
from portfolio.models.events import Events
from portfolio.models.organisation import Organisation
from portfolio.models.request_to_organisation import RequestToOrganisation


def get_response_get_list_organisations(organisations: List[Organisation]):
    return OrganisationSerializer.serialize(organisations, SER_FOR_GET_LIST_ORGANISATION)


def get_response_get_detail_organisation(organisation: Organisation):
    return OrganisationSerializer.serialize(organisation, SER_FOR_GET_DETAIL_ORGANISATION)


def get_response_get_list_events(list_events: List[Events]):
    return EventsSerializer.serialize(list_events, SER_FOR_GET_LIST_EVENTS)


def get_response_get_detail_event(event: Events):
    return EventsSerializer.serialize(event, SER_FOR_GET_DETAIL_EVENT)


def get_response_make_request(request_to_organisation: RequestToOrganisation):
    return RequestToOrganisationSerializer.serialize(request_to_organisation, SER_FOR_MAKE_REQUEST)


def get_response_add_achievements(achievement: Achievements):
    return AchievementsSerializer.serialize(achievement, SER_FOR_ADD_ACHIEVEMENT)
