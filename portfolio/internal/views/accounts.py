from flask import Request, render_template, Blueprint, request, json, Response, make_response

from portfolio.internal.biz.deserializers.account_main import AccountMainDeserializer, DES_FROM_REGISTER, \
    DES_FROM_LOGIN, DES_FROM_RECOVERY_PASSWORD
from portfolio.internal.biz.services.account_service import AccountService
from portfolio.internal.biz.services.auth_service import AuthService
from portfolio.internal.biz.validators.confirm_code import ConfirmCodeSchema
from portfolio.internal.biz.validators.login import LoginAuthSchema
from portfolio.internal.biz.validators.recovery_password import RecoveryPasswordSchema
from portfolio.internal.biz.validators.register import RegisterAuthSchema
from portfolio.internal.middlewares.auth import required_auth, required_auth_with_unconfirmed_email
from portfolio.internal.views.answers.account import get_response_register, get_response_account_detail, \
    get_response_login, get_response_recovery_password
from portfolio.models.account_main import AccountMain
from portfolio.models.auth_code import AuthCode

account = Blueprint('account', __name__, template_folder="../../templates/account/", static_folder="../../static/account/")


@account.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        errors = RegisterAuthSchema().validate(dict(name=request.form['name'],
                                                    email=request.form['email'],
                                                    password=request.form['password']))
        if errors:
            return json.dumps(errors)

        account_main = AccountMainDeserializer.deserialize(request.form, DES_FROM_REGISTER)
        account_main, errors = AuthService.register(account_main)
        if errors:
            return json.dumps(errors)
        response = Response(response=json.dumps(get_response_register(account_main)),
                            status=200,
                            mimetype='application/json')
        return render_template('registration.html',
                               context=response.response,
                               status_code=response.status_code,
                               mimetype=response.mimetype)
    return render_template('registration.html', errors=None)


@account.route('/auth/code', methods=['POST'])
@required_auth
def confirm_code(auth_account_main_id: int):
    validate_errors = ConfirmCodeSchema().validate(dict(code=request.form.get('code')))
    if validate_errors:
        return json.dumps(validate_errors)

    auth_code = AuthCode(account_main=AccountMain(id=auth_account_main_id),
                         code=request.form.get('code'))
    _, err = AuthService.confirm_code(auth_code)
    if err:
        return json.dumps(err)

    return json.dumps(True)


@account.route('/auth/new_code', methods=['POST'])
@required_auth_with_unconfirmed_email
def send_new_code(auth_account_main_id: int):
    _, err = AuthService.send_new_auth_code(auth_account_main_id)
    if err:
        return json.dumps(err)

    return json.dumps(True)


@account.route("/detail", methods=['GET'])
@required_auth
def get_detail_info(auth_account_main_id: int):
    account_main, err = AccountService.get_detail_account_info(auth_account_main_id)
    if err:
        return json.dumps(err)

    return json.dumps(get_response_account_detail(account_main))


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        errors = LoginAuthSchema().validate(dict(email=request.form['email'],
                                                 password=request.form['password']))
        if errors:
            return json.dumps(errors)

        account_main = AccountMainDeserializer.deserialize(request.form, DES_FROM_LOGIN)
        account_main, err = AuthService.auth_login(account_main)
        if err:
            return json.dumps(err)
        response = Response(response=json.dumps(get_response_login(account_main)),
                            status=200,
                            mimetype='application/json')
        return render_template('account/login.html',
                               context=response.response,
                               status_code=response.status_code,
                               mimetype=response.mimetype)
    return render_template('account/login.html', errors=None)


@account.route('/recovery_password', methods=['GET', 'POST'])
def recovery_password():
    if request.method == 'POST':
        errors = RecoveryPasswordSchema().validate(dict(email=request.form['email'],
                                                        name=request.form['name']))
        if errors:
            return json.dumps(errors)

        account_main = AccountMainDeserializer.deserialize(request.form, DES_FROM_RECOVERY_PASSWORD)
        account_main, err = AuthService.recovery_password(account_main)
        if err:
            return json.dumps(err)
        response = Response(response=json.dumps(get_response_recovery_password(account_main)),
                            status=200,
                            mimetype='application/json')
        return render_template('account/password.html',
                               context=response.response,
                               status_code=response.status_code,
                               mimetype=response.mimetype)
    return render_template('account/password.html', errors=None)
