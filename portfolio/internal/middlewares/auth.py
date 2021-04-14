from flask import request

from portfolio.internal.biz.services.auth_service import AuthService
from portfolio.models.account_session import AccountSession


def required_auth(func):
    def wrapper(*args, **kwargs):
        if not request.headers.get('auth-token'):
            return "Где токен?"

        session_id = AccountSession.get_session_id_from_token(request.headers.get('auth-token'))
        if not session_id:
            return "Невалидный или устаревший токен"

        account_main, err = AuthService.get_account_main_by_session_id(session_id)
        if err:
            return "HZ"

        if not account_main:
            return "Невалидный или устаревший токен"

        response = func(*args, auth_account_main_id=account_main.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper


def required_auth_with_unconfirmed_email(func):
    def wrapper(*args, **kwargs):
        if not request.headers.get('auth-token'):
            return "Где токен?"

        session_id = AccountSession.get_session_id_from_token(request.headers.get('auth-token'))
        if not session_id:
            return "Невалидный или устаревший токен"

        account_main, err = AuthService.get_account_main_by_session_id_with_confirmed(session_id)
        if err:
            return "HZ"

        if not account_main:
            return "Невалидный или устаревший токен"

        if account_main.is_confirmed:
            return "Email Уже подтвержден"

        response = func(*args, auth_account_main_id=account_main.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper


def required_auth_with_confirmed_email(func):
    async def wrapper(request, *args, **kwargs):
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

        response = func(request, *args, auth_account_main_id=account_main.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper
