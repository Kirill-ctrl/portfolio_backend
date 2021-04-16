from datetime import datetime

from flask import Blueprint, request, json

from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FOR_ADD_CHILD
from portfolio.internal.biz.services.children_service import ChildrenService
from portfolio.internal.biz.services.events_child import EventsChildService
from portfolio.internal.biz.services.request_to_organisation import RequestToOrganisationService
from portfolio.internal.biz.validators.add_child import AddChildSchema
from portfolio.internal.middlewares.parents import get_parent_id_and_account_main_id
from portfolio.internal.middlewares.statistic_and_focus import get_sort_statistic, get_sort_focus
from portfolio.internal.views.answers.children import get_response_add_children, get_response_detail_activity_children
from portfolio.models.account_main import AccountMain
from portfolio.models.children import Children
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events_child import EventsChild
from portfolio.models.parents import Parents

private_office_parents = Blueprint('parents/private_office', __name__, template_folder='templates/private_office', static_folder='static/private_office')


@private_office_parents.route('/', methods=['GET', 'POST'])
@get_parent_id_and_account_main_id
def index(parent_id: int, auth_account_main_id: int):
    if request.method == 'POST':
        errors = AddChildSchema().validate(dict(name=request.form['name'],
                                                surname=request.form['surname'],
                                                date_born=request.form['date_born']))
        if errors:
            return json.dumps(errors)
        children = ChildrenDeserialize.deserialize(request.form, DES_FOR_ADD_CHILD)
        children.parents = Parents(id=parent_id, account_main=AccountMain(id=auth_account_main_id))
        children, err = ChildrenService.add_child(children)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_add_children(children))


@private_office_parents.route('/request_add_child', methods=['POST'])
@get_parent_id_and_account_main_id
def request_add_child(parent_id: int, auth_account_main_id: int):
    if request.method == 'POST':
        children_name = request.args.get('name')
        event_name = request.args.get('event')
        children = Children(name=children_name,
                            parents=Parents(id=parent_id,
                                            account_main=AccountMain(id=auth_account_main_id)))
        children, err = ChildrenService.get_child(children)
        if err:
            return json.dumps(err)

        request_to_organisation, err = RequestToOrganisationService.make_request(children)
        if err:
            return json.dumps(err)


@private_office_parents.route('/children/<int:children_id>', methods=['GET', 'POST'])
@get_parent_id_and_account_main_id
@get_sort_statistic
@get_sort_focus
def detail_child(result_sort_statistic: datetime.date, result_sort_focus: datetime.date, parent_id: int, auth_account_main_id: int, children_id: int):
    if request.method == 'GET':
        events_child = EventsChild(
            children_organisation=ChildrenOrganisation(
                children=Children(
                    id=children_id
                )
            )
        )
        activity_child, err = EventsChildService.get_by_children_id(events_child)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_detail_activity_children(activity_child))

    # TODO Проверяем участовал ли ребенок в мероприятиях в дао children_organisation, may null
    # TODO Добавить статистику, достяги, фокус
