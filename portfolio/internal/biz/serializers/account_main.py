from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.account_main import AccountMain

SER_FOR_REGISTER = 'ser-for-register'
SER_FOR_LOGIN = 'ser-for-login'
SER_FOR_DETAIL = 'ser-for-detail'
SER_FOR_RECOVERY_PASSWORD = 'ser-for-recovery-password'


class AccountMainSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_REGISTER:
            return cls._ser_for_register
        elif format_ser == SER_FOR_DETAIL:
            return cls._ser_for_detail
        elif format_ser == SER_FOR_LOGIN:
            return cls._ser_for_login
        elif format_ser == SER_FOR_RECOVERY_PASSWORD:
            return cls._ser_for_recovery_password
        else:
            return TypeError

    @staticmethod
    def _ser_for_register(account_main: AccountMain) -> dict:
        return {
            'id': account_main.id,
            'email': account_main.email,
            'auth_token': account_main.auth_token,
            'is_confirmed': account_main.is_confirmed,
            'is_email_sent': account_main.is_email_sent if account_main.is_email_sent is not None else False
        }

    @staticmethod
    def _ser_for_detail(account_main: AccountMain) -> dict:
        return {
            'id': account_main.id,
            'created_at': account_main.created_at,
            'edited_at': account_main.edited_at,
            'email': account_main.email,
            'name': account_main.name,
            'is_confirmed': account_main.is_confirmed,
        }

    @staticmethod
    def _ser_for_login(account_main: AccountMain) -> dict:
        return {
            'id': account_main.id,
            'email': account_main.email,
            'auth_token': account_main.auth_token,
            'name': account_main.name,
            'is_confirmed': account_main.is_confirmed
        }

    @staticmethod
    def _ser_for_recovery_password(account_main: AccountMain) -> dict:
        return {
            'id': account_main.id,
            'email': account_main.email,
            'name': account_main.name,
            'is_email_sent': account_main.is_email_sent
        }
