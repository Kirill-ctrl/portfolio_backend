from typing import List

from portfolio.internal.biz.serializers.request_to_organisation import RequestToOrganisationSerializer, \
    SER_FOR_GET_ALL_REQUESTS, SER_FOR_ACCEPT_REQUEST
from portfolio.models.request_to_organisation import RequestToOrganisation


def get_response_with_get_all_requests(list_request_to_organisation: List[RequestToOrganisation]):
    return RequestToOrganisationSerializer.serialize(list_request_to_organisation, SER_FOR_GET_ALL_REQUESTS)


def get_response_accept_request(request_to_organisation: RequestToOrganisation):
    return RequestToOrganisationSerializer.serialize(request_to_organisation, SER_FOR_ACCEPT_REQUEST)