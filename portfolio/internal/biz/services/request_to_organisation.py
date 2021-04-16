from portfolio.drivers.mail_server import MailServer, EMAIL_ACCEPT_REQUEST
from portfolio.internal.biz.dao.children import ChildrenDao
from portfolio.internal.biz.dao.request_to_organisation import RequestToOrganisationDao
from portfolio.models.request_to_organisation import RequestToOrganisation


class RequestToOrganisationService:

    @staticmethod
    def make_request(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().add(request_to_organisation)
        if err:
            return None, err
        return request_to_organisation, None

    @staticmethod
    def get_all_requests_by_org_id(request_to_organisation: RequestToOrganisation):
        list_request_to_organisation, err = RequestToOrganisationDao().get_all_request_by_org_id(request_to_organisation)
        if err:
            return None, err

        tuple_children_id = tuple([request.children.id for request in list_request_to_organisation])
        print(tuple_children_id)
        list_children, err = ChildrenDao().get_list_by_tuple_children_id(tuple_children_id)
        if err:
            return None, err

        for req, child in list(zip(list_request_to_organisation, list_children)):
            req.children.id = child.id
            req.children.name = child.name
            req.children.surname = child.surname
            req.children.date_born = child.date_born

        return list_request_to_organisation, None

    @staticmethod
    def accept_request(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().accept_request(request_to_organisation)
        if err:
            return None, err

        request_to_organisation.parents.account_main.is_email_sent = MailServer.send_email(EMAIL_ACCEPT_REQUEST,
                                                                                           request_to_organisation.parents.account_main.email,
                                                                                           request_to_organisation.status)

        return request_to_organisation, None
