from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.request_to_organisation import RequestToOrganisation

SER_FOR_MAKE_REQUEST = 'ser-for-make-request'
SER_FOR_GET_ALL_REQUESTS = 'ser-for-get-all-requests'
SER_FOR_ACCEPT_REQUEST = 'ser-for-accept-request'


class RequestToOrganisationSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_MAKE_REQUEST:
            return cls._ser_for_make_request
        elif format_ser == SER_FOR_GET_ALL_REQUESTS:
            return cls._ser_for_get_all_requests
        elif format_ser == SER_FOR_ACCEPT_REQUEST:
            return cls._ser_for_accept_request
        else:
            raise TypeError

    @staticmethod
    def _ser_for_make_request(request_to_organisation: RequestToOrganisation) -> dict:
        return {
            'id': request_to_organisation.id,
            'created_at': request_to_organisation.created_at,
            'edited_at': request_to_organisation.edited_at,
            'parents': {
                'id': request_to_organisation.parents.id
            },
            'events': {
                'id': request_to_organisation.events.id
            },
            'children': {
                'id': request_to_organisation.children.id
            }
        }

    @staticmethod
    def _ser_for_get_all_requests(list_request_to_organisation):
        return {
            'organisation': {
                'id': list_request_to_organisation[0].events.organisation.id,
            },
            'request_to_organisation': {
                'requests': [
                    {
                        'id': list_request_to_organisation[i].id,
                        'status': list_request_to_organisation[i].status,
                        'parents': {
                            'id': list_request_to_organisation[i].parents.id,
                            'name': list_request_to_organisation[i].parents.name,
                            'surname': list_request_to_organisation[i].parents.surname
                        },
                        'events': {
                            'id': list_request_to_organisation[i].events.id,
                            'name': list_request_to_organisation[i].events.name,
                            'surname': list_request_to_organisation[i].events.date_event
                        },
                        'children': {
                            'id': list_request_to_organisation[i].children.id,
                            'name': list_request_to_organisation[i].children.name,
                            'surname': list_request_to_organisation[i].children.surname
                        }
                    }
                    for i in range(len(list_request_to_organisation))
                ]
            }
        }

    @staticmethod
    def _ser_for_accept_request(request_to_organisation):
        return {
            'request': {
                'id': request_to_organisation.id,
                'status': request_to_organisation.status
            }
        }
