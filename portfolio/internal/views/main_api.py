from typing import List

from flask import Blueprint, request, json, url_for, redirect

from portfolio.internal.biz.services.events import EventsService
from portfolio.internal.biz.services.organisation import OrganisationService
from portfolio.internal.biz.services.request_to_organisation import RequestToOrganisationService
from portfolio.internal.middlewares.auth import required_auth_with_confirmed_email, required_auth
from portfolio.internal.middlewares.parents import get_parent_id_and_account_main_id, check_child_by_parent
from portfolio.internal.middlewares.request import get_query_params_search_organisation, get_query_params_search_event
from portfolio.internal.views.answers.main_api import get_response_get_list_organisations, \
    get_response_get_detail_organisation, get_response_get_list_events, get_response_get_detail_event, \
    get_response_make_request
from portfolio.models.children import Children
from portfolio.models.events import Events
from portfolio.models.events_child import EventsChild
from portfolio.models.organisation import Organisation
from portfolio.models.parents import Parents
from portfolio.models.request_to_organisation import RequestToOrganisation

main = Blueprint('main', __name__, template_folder='templates/main', static_folder='static/main')


@main.route('/organisations', methods=['GET'])
@required_auth_with_confirmed_email
@get_query_params_search_organisation
def list_organisation(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        if organisation_id:
            return redirect(url_for('detail_organisation', organisation_id=organisation_id))

        organisations, err = OrganisationService.get_all_organisations()

        if err:
            return json.dumps(err)

        return json.dumps(get_response_get_list_organisations(organisations))


@main.route('/organisations/<int:organisation_id>', methods=['GET'])
@required_auth_with_confirmed_email
def detail_organisation(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        organisation, err = OrganisationService.get_by_organisation_id(organisation_id)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_get_detail_organisation(organisation))


@main.route('/organisations/<int:organisation_id>/events', methods=['GET'])
@required_auth_with_confirmed_email
@get_query_params_search_event
def get_list_events(organisation_id: int, events_id: int):
    if request.method == 'GET':
        if events_id:
            return redirect(url_for('detail_event', organisation_id=organisation_id, events_id=events_id))
        list_events, err = EventsService.get_all_events_by_organisation_id(organisation_id)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_get_list_events(list_events))


@main.route('/organisations/<int:organisation_id>/events/<int:events_id>', methods=['GET'])
@required_auth_with_confirmed_email
def detail_event(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'GET':
        event, err = EventsService.get_by_events_id(events_id)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_get_detail_event(event))


@main.route('/organisations/<int:organisation_id>/events/<int:events_id>/make_request', methods=['POST', 'GET'])
@check_child_by_parent
def make_request(organisation_id, events_id, parent_id: int, list_children: List[Children]):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        children_id = request.args.get('children_id')
        if not children_id:
            return json.dumps('Как вы это сделали?')
        select_child = None
        for child in list_children:
            if child.id == children_id:
                select_child = child
        if not select_child:
            return json.dumps('Добавьте сначала ребенка в личном кабинете')
        request_to_organisation = RequestToOrganisation(
            parents=Parents(id=parent_id),
            events=Events(id=events_id,
                          organisation=Organisation(id=organisation_id)),
            children=Children(id=select_child.id)
        )
        request_to_organisation, err = RequestToOrganisationService.make_request(request_to_organisation)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_make_request(request_to_organisation))
