from flask import Blueprint, request, json

from portfolio.internal.biz.deserializers.achievements import AchievementsDeserializer, DES_FROM_ADD_ACHIEVEMENT
from portfolio.internal.biz.deserializers.events import EventDeserializer, DES_FROM_ADD_EVENT
from portfolio.internal.biz.deserializers.teacher import TeacherDeserializer, DES_FOR_ADD_TEACHER, DES_FOR_EDIT_TEACHER
from portfolio.internal.biz.serializers.utils import SetEncoder
from portfolio.internal.biz.services.achievements import AchievementService
from portfolio.internal.biz.services.children_organisation import ChildrenOrganisationService
from portfolio.internal.biz.services.events import EventsService
from portfolio.internal.biz.services.events_child import EventsChildService
from portfolio.internal.biz.services.organisation import OrganisationService
from portfolio.internal.biz.services.request_to_organisation import RequestToOrganisationService
from portfolio.internal.biz.services.teacher import TeacherService
from portfolio.internal.biz.validators.add_achievement import AddAchievementSchema
from portfolio.internal.biz.validators.private_office_organisation import AddTeacherSchema, EditTeacherSchema, \
    AddChildrenSchema, AddEventSchema
from portfolio.internal.middlewares.auth import required_auth_with_confirmed_email
from portfolio.internal.middlewares.organisation import get_org_id_and_acc_id_with_confirmed_email
from portfolio.internal.middlewares.private_office_organisation import get_teacher_id_and_org_id
from portfolio.internal.views.answers.children_organisation import get_response_list_children_organisation, \
    get_response_detail_activity_child_organisation
from portfolio.internal.views.answers.events import get_response_add_event
from portfolio.internal.views.answers.events_child import get_response_add_activity
from portfolio.internal.views.answers.main_api import get_response_get_list_events, get_response_get_detail_event, \
    get_response_add_achievements
from portfolio.internal.views.answers.request_to_organisation import get_response_with_get_all_requests, \
    get_response_accept_request
from portfolio.internal.views.answers.teacher import get_response_add_teacher, get_response_edit_teacher, \
    get_response_delete_teacher, get_response_detail_organisation
from portfolio.models.account_main import AccountMain
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events import Events
from portfolio.models.events_child import EventsChild
from portfolio.models.organisation import Organisation
from portfolio.models.request_to_organisation import RequestToOrganisation
from portfolio.models.teacher import Teacher

private_office_organisation = Blueprint('organisation/private_office', __name__, template_folder='templates/organisation/private_office', static_folder='static/organisation/private_office')


@private_office_organisation.route('/add_teacher', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def add_teacher(auth_account_main_id: int, organisation_id: int):
    if request.method == 'POST':
        errors = AddTeacherSchema().validate(dict(name=request.form['name'],
                                                  surname=request.form['surname'],
                                                  specialty=request.form['specialty']))
        if errors:
            return json.dumps(errors)
        teacher = TeacherDeserializer.deserialize(request.form, DES_FOR_ADD_TEACHER)
        teacher.organisation = Organisation(id=organisation_id,
                                            account_main=AccountMain(id=auth_account_main_id))
        teacher, err = TeacherService.add_teacher(teacher)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_add_teacher(teacher))


@private_office_organisation.route('/edit_teacher')
@get_org_id_and_acc_id_with_confirmed_email
def edit_teacher(auth_account_main_id: int, organisation_id: int):
    errors = EditTeacherSchema().validate(dict(name=request.form['name'],
                                               surname=request.form['surname'],
                                               specialty=request.form['specialty']))
    if errors:
        return json.dumps(errors)
    teacher = TeacherDeserializer.deserialize(request.form, DES_FOR_EDIT_TEACHER)
    teacher.organisation = Organisation(id=organisation_id,
                                        account_main=AccountMain(id=auth_account_main_id))
    teacher, err = TeacherService.edit_teacher(teacher)
    if err:
        return json.dumps(err)
    return json.dumps(get_response_edit_teacher(teacher))


@private_office_organisation.route('/delete_teacher')
@get_org_id_and_acc_id_with_confirmed_email
def delete_teacher(auth_account_main_id: int, organisation_id: int):
    teacher = Teacher(organisation=Organisation(id=organisation_id,
                                                account_main=AccountMain(id=auth_account_main_id)))
    teacher, err = TeacherService.delete_teacher(teacher)
    if err:
        return json.dumps(err)
    return json.dumps(get_response_delete_teacher(teacher))


@private_office_organisation.route('/', methods=['GET'])
@required_auth_with_confirmed_email
def main_page(auth_account_main_id: int):
    if request.method == 'GET':
        organisation = Organisation(account_main=AccountMain(id=auth_account_main_id))

        list_teacher_organisation, err = OrganisationService.get_all_by_account_id(organisation.account_main.id)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_detail_organisation(list_teacher_organisation))


@private_office_organisation.route('/add_event', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def add_event(auth_account_main_id: int, organisation_id: int):
    if request.method == 'POST':
        errors = AddEventSchema().validate(dict(type=request.form['type'],
                                                name=request.form['name'],
                                                date_event=request.form['date_event'],
                                                event_hours=request.form['hours'],
                                                skill=request.form['skill']))
        if errors:
            return json.dumps(errors)
        event: Events = EventDeserializer.deserialize(request.form, DES_FROM_ADD_EVENT)
        event.organisation = Organisation(id=organisation_id,
                                          account_main=AccountMain(id=auth_account_main_id))
        event, err = EventsService.add_event(event)
        if err:
            return None, err

        return json.dumps(get_response_add_event(event))


@private_office_organisation.route('/requests', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_requests(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        request_to_organisation = RequestToOrganisation(
            events=Events(organisation=Organisation(
                id=organisation_id,
                account_main=AccountMain(id=auth_account_main_id)
            ))
        )
        list_request_to_organisation, err = RequestToOrganisationService.get_all_requests_by_org_id(request_to_organisation)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_with_get_all_requests(list_request_to_organisation))


@private_office_organisation.route('/requests/<int:request_id>', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_detail_request(auth_account_main_id: int, organisation_id: int, request_id: int):
    if request.method == 'POST':
        request_to_organisation = RequestToOrganisation(
            id=request_id,
            events=Events(organisation=Organisation(
                id=organisation_id,
                account_main=AccountMain(id=auth_account_main_id)
            ))
        )
        # TODO статус = тру, достаем id ребенка для events_child,
        request_to_organisation, err = RequestToOrganisationService.accept_request(request_to_organisation)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_accept_request(request_to_organisation))


@private_office_organisation.route('/learners', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_list_learners(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        list_learners, err = ChildrenOrganisationService.get_all_by_org_id(organisation_id)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_list_children_organisation(list_learners))


@private_office_organisation.route('/learners/<int:children_org_id>', methods=['GET'])
def get_detail_children(children_org_id: int):
    if request.method == 'GET':
        list_activity_child, err = EventsChildService.get_by_children_org_id(children_org_id)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_detail_activity_child_organisation(list_activity_child), cls=SetEncoder)


@private_office_organisation.route('/learners/<int:children_org_id>/add_activity', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def add_activity(auth_account_main_id: int, organisation_id: int, children_org_id: int):
    if request.method == 'POST':
        event_id = request.args.get('event_id')
        if not event_id:
            return json.dumps("Сначала выберите событие")

        events_child = EventsChild(
            children_organisation=ChildrenOrganisation(
                id=children_org_id,
            ),
            events=Events(id=event_id)
        )

        activity_child, err = EventsChildService.update_status(events_child)
        if err:
            json.dumps(err)
        return json.dumps(get_response_add_activity(activity_child))
        # TODO Как вариант берем account_main.email и отправляем, что у нас новая активность


@private_office_organisation.route('/events', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_list_events(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        list_events, err = EventsService.get_all_events_by_organisation_id(organisation_id)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_get_list_events(list_events))


@private_office_organisation.route('events/<int:events_id>', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def detail_event(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'GET':
        event, err = EventsService.get_by_events_id(events_id)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_get_detail_event(event))


@private_office_organisation.route('events/<int:events_id>/add_achievement', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def add_achievement(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'POST':
        errors = AddAchievementSchema().validate(dict(name=request.form['name'],
                                                      point=request.form['point'],
                                                      nomination=request.form['nomination']))
        if errors:
            return json.dumps(errors)
        achievement = AchievementsDeserializer.deserialize(request.form, DES_FROM_ADD_ACHIEVEMENT)
        achievement.events = Events(id=events_id)
        achievement, err = AchievementService.add_achievement(achievement)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_add_achievements(achievement))
