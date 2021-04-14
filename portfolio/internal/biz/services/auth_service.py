from portfolio.configs.intenal import LIFETIME_CODE, SEND_CODE_INTERVAL
from portfolio.drivers.mail_server import MailServer, EMAIL_CODE_TYPE, EMAIL_RECOVERY_PASSWORD_TYPE
from portfolio.internal.biz.dao.account_main import AccountMainDao
from portfolio.internal.biz.dao.account_session import AccountSessionDao
from portfolio.internal.biz.dao.auth_code import AuthCodeDao
from portfolio.internal.biz.services.utils import get_passed_time, get_temp_password
from portfolio.models.account_main import AccountMain
from portfolio.models.account_session import AccountSession
from portfolio.models.auth_code import AuthCode


class AuthService:
    @staticmethod
    def register(account_main: AccountMain):
        account_main.create_hash_password()
        account_main.is_confirmed = False
        account_main, errors = AuthService._add_account_main_and_create_session(account_main)
        if errors:
            return None, errors

        auth_code = AuthCode(account_main=account_main)
        auth_code.create_random_code()

        _, errors = AuthCodeDao().add(auth_code)
        if errors:
            return None, errors

        account_main.is_email_sent = MailServer.send_email(EMAIL_CODE_TYPE, account_main.email, auth_code.code)

        return account_main, None

    @staticmethod
    def auth_login(account_main: AccountMain):
        account_main.create_hash_password()
        account_main, err = AccountMainDao().get_by_email_and_hash_password(account_main)
        if err:
            return None, err

        if not account_main:
            return None, "Неверный email"

        account_session = AccountSession(account_main=account_main)
        account_session, err = AccountSessionDao().add(account_session)
        if err:
            return None, err

        account_main.auth_token = account_session.create_token()

        return account_main, None

    @staticmethod
    def recovery_password(account_main: AccountMain):
        account_main, err = AccountMainDao().get_by_email_and_name(account_main)
        if err:
            return None, err

        if not account_main:
            return None, "Неверный email"

        if not account_main.is_confirmed:
            return None, "email не подтвержден"

        account_main.password = get_temp_password()
        account_main.create_hash_password()
        account_main, err = AccountMainDao().set_temp_psw(account_main)
        if err:
            return None, err

        account_main.is_email_sent = MailServer.send_email(EMAIL_RECOVERY_PASSWORD_TYPE, account_main.email, account_main.password)

        return account_main, None

    @staticmethod
    def _add_account_main_and_create_session(account_main: AccountMain):
        account_main, errors = AccountMainDao().add(account_main)
        if errors:
            return None, errors
        account_main, errors = AuthService._create_session(account_main)
        if errors:
            return None, errors

        return account_main, None

    @staticmethod
    def _create_session(account_main: AccountMain):
        account_session = AccountSession(account_main=account_main)
        account_session, err = AccountSessionDao().add(account_session)
        if err:
            return None, err

        account_main.auth_token = account_session.create_token()

        return account_main, None

    @staticmethod
    def confirm_code(auth_code: AuthCode):
        auth_code, err = AuthCodeDao().get_code_by_account_main_id(auth_code)
        if err:
            return None, err

        if not auth_code:
            return None, "Указан неизвестный код подтверждения"

        if get_passed_time(auth_code.edited_at) > LIFETIME_CODE:
            return None, "Код недействителен"

        _, err = AuthCodeDao().set_is_confirm(auth_code.account_main.id, True)
        if err:
            return None, "Ошибочка"

        _, err = AuthCodeDao().remove_by_id(auth_code.id)
        if err:
            return None, "Не удалилось"

        return None, None

    @staticmethod
    def get_account_main_by_session_id(session_id: int):
        account_main, err = AccountMainDao().get_by_session_id(session_id)
        if err:
            return None, "Не нашелся аккаунт"

        return account_main, None

    @staticmethod
    def get_account_main_by_session_id_with_confirmed(session_id: int):
        account_main, err = AccountMainDao().get_by_session_id_with_confirmed(session_id)
        if err:
            return None, err

        return account_main, None

    @staticmethod
    def send_new_auth_code(auth_account_main_id: int):
        main_code, err = AuthCodeDao().get_by_account_main_id(auth_account_main_id)
        if err:
            return None, err

        if main_code and get_passed_time(main_code.edited_at) < SEND_CODE_INTERVAL:
            return None, "Сообщения можно отправлять не чаще, чем раз в 60 секунд"

        auth_code = AuthCode(account_main=AccountMain(id=auth_account_main_id))
        auth_code.create_random_code()

        if main_code:
            _, err = AuthCodeDao().update(main_code.id, auth_code)
        else:
            _, err = AuthCodeDao().add(auth_code)

        account_main, err = AccountMainDao().get_email_by_id(auth_account_main_id)
        if err:
            return None, err

        _ = MailServer.send_email(EMAIL_CODE_TYPE, account_main.email, auth_code.code)

        return None, None
