from flask import json, request

from portfolio.internal.biz.services.auth_service import AuthService
from portfolio.internal.biz.services.parents import ParentsService
from portfolio.models.account_session import AccountSession


def get_parent_id_and_account_main_id(func):
    def wrapper(*args, **kwargs):
        if not request.headers.get('auth-token'):
            return "Где токен?"

        session_id = AccountSession.get_session_id_from_token(request.headers.get('auth-token'))
        if not session_id:
            return "Невалидный или недействительный токен"

        account_main, err = AuthService.get_account_main_by_session_id_with_confirmed(session_id)
        if err:
            return "HZ"

        if not account_main:
            return "Невалидный или недействительный токен"

        if not account_main.is_confirmed:
            return "Пожалуйста, подтвердите email"

        parent, err = ParentsService.get_by_account_id(account_main.id)
        if err:
            return json.dumps(err)

        response = func(*args, auth_account_main_id=account_main.id, parent_id=parent.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper
