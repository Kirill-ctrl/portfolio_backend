from flask import Blueprint, request, json

from portfolio.internal.biz.deserializers.parents import ParentsDeserializer, DES_FROM_ADD_PARENTS, \
    DES_FROM_EDIT_PARENTS
from portfolio.internal.biz.services.parents import ParentsService
from portfolio.internal.biz.validators.add_parents import AddParentsSchema
from portfolio.internal.biz.validators.edit_parents import EditParentsSchema
from portfolio.internal.middlewares.auth import required_auth_with_confirmed_email
from portfolio.internal.views.answers.parents import get_response_add_parents, get_response_edit_parent, \
    get_response_delete_parent
from portfolio.models.account_main import AccountMain
from portfolio.models.parents import Parents

parents = Blueprint('parents', __name__, template_folder='templates/parents', static_folder='static/parents')


@parents.route('/add_parents', methods=['POST', 'GET'])
@required_auth_with_confirmed_email
def add_parents(auth_account_main_id: int):
    if request.method == 'POST':
        errors = AddParentsSchema().validate(dict(name=request.form['name'],
                                                  surname=request.form['surname']))
        if errors:
            return json.dumps(errors)
        parent = ParentsDeserializer.deserialize(request.form, DES_FROM_ADD_PARENTS)
        parent.account_main = AccountMain(id=auth_account_main_id)
        parent, err = ParentsService.add_parent(parent)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_add_parents(parent))


@parents.route('/edit_parents', methods=['POST', 'GET'])
@required_auth_with_confirmed_email
def edit_parents(auth_account_main_id: int):
    if request.method == 'POST':
        errors = EditParentsSchema().validate(dict(name=request.form['name'],
                                                   surname=request.form['surname']))
        if errors:
            return json.dumps(errors)
        parent = ParentsDeserializer.deserialize(request.form, DES_FROM_EDIT_PARENTS)
        parent.account_main = AccountMain(id=auth_account_main_id)
        parent, err = ParentsService.update_parent(parent)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_edit_parent(parent))


@parents.route('/delete_parents', methods=['DELETE', 'GET'])
@required_auth_with_confirmed_email
def del_parents(auth_account_main_id: int):
    if request.method == 'DELETE':
        parent = Parents(account_main=AccountMain(id=auth_account_main_id))
        parent, err = ParentsService.delete_parent(parent)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_delete_parent(parent))
