from flask import Blueprint, request, json

from portfolio.internal.biz.deserializers.organisation import OrganisationDeserializer, DES_FROM_ADD_ORGANISATION, \
    DES_FOR_EDIT_ORGANISATION
from portfolio.internal.biz.services.organisation import OrganisationService
from portfolio.internal.biz.validators.add_organisation import AddOrganisationSchema
from portfolio.internal.biz.validators.edit_organisation import EditOrganisationSchema
from portfolio.internal.middlewares.auth import required_auth_with_confirmed_email
from portfolio.internal.views.answers.organisation import get_response_add_organisation, get_response_edit_organisation, \
    get_response_delete_organisation
from portfolio.models.account_main import AccountMain
from portfolio.models.organisation import Organisation

organisation = Blueprint('organisation', __name__, template_folder='templates/organisation', static_folder='static/organisation')


@organisation.route('/add_organisation', methods=['POST', 'GET'])
@required_auth_with_confirmed_email
def add_organisation(auth_account_main_id: int):
    if request.method == 'POST':
        errors = AddOrganisationSchema().validate(dict(name=request.form['name'],
                                                       login=request.form['login'],
                                                       photo_link=request.form['photo_link'],
                                                       description=request.form['description']))
        if errors:
            return json.dumps(errors)
        organisations = OrganisationDeserializer.deserialize(request.form, DES_FROM_ADD_ORGANISATION)
        organisations.account_main = AccountMain(id=auth_account_main_id)
        organisations, err = OrganisationService.add_organisation(organisations)
        if err:
            return json.dumps(err)

        return get_response_add_organisation(organisations)


@organisation.route('/edit_organisation', methods=['POST', 'GET'])
@required_auth_with_confirmed_email
def edit_organisation(auth_account_main_id: int):
    if request.method == 'POST':
        errors = EditOrganisationSchema().validate(dict(name=request.form['name'],
                                                        login=request.form['login'],
                                                        photo_link=request.form['photo_link'],
                                                        description=request.form['description']))
        if errors:
            return json.dumps(errors)
        organisations = OrganisationDeserializer.deserialize(request.form, DES_FOR_EDIT_ORGANISATION)
        organisations.account_main = AccountMain(id=auth_account_main_id)
        organisations, err = OrganisationService.edit_organisation(organisations)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_edit_organisation(organisations))


@organisation.route('/delete_organisation', methods=['POST', 'GET'])
@required_auth_with_confirmed_email
def delete_organisation(auth_account_main_id: int):
    if request.method == 'POST':
        organisations = Organisation(account_main=AccountMain(id=auth_account_main_id))
        organisations, err = OrganisationService.delete_organisation(organisations)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_delete_organisation(organisations))
