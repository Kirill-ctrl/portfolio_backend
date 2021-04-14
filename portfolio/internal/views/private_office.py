from flask import Blueprint, request, json

from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FOR_ADD_CHILD
from portfolio.internal.biz.services.children_service import ChildrenService
from portfolio.internal.biz.validators.add_child import AddChildSchema
from portfolio.internal.middlewares.parents import get_parent_id_and_account_main_id
from portfolio.internal.views.answers.children import get_response_add_children
from portfolio.models.account_main import AccountMain
from portfolio.models.parents import Parents

private_office = Blueprint('private_office', __name__, template_folder='templates/private_office', static_folder='static/private_office')


@private_office.route('/', methods=['GET', 'POST'])
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
