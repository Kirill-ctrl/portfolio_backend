from portfolio.internal.biz.serializers.organisation import SER_FOR_ADD_ORGANISATION, OrganisationSerializer, \
    SER_FOR_EDIT_ORGANISATION, SER_FOR_DELETE_ORGANISATION
from portfolio.models.organisation import Organisation


def get_response_add_organisation(organisation: Organisation):
    return OrganisationSerializer.serialize(organisation, SER_FOR_ADD_ORGANISATION)


def get_response_edit_organisation(organisation: Organisation):
    return OrganisationSerializer.serialize(organisation, SER_FOR_EDIT_ORGANISATION)


def get_response_delete_organisation(organisation: Organisation):
    return OrganisationSerializer.serialize(organisation, SER_FOR_DELETE_ORGANISATION)
