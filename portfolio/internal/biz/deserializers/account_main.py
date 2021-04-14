from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.account_main import AccountMain

DES_FROM_REGISTER = "des-from-register"
DES_FROM_LOGIN = "des-from-login"
DES_ACCOUNT_MAIN_FROM_DB_FULL = 'des-account-main-from-db-full'
DES_FROM_RECOVERY_PASSWORD = 'des-from-recovery-password'


class AccountMainDeserializer(BaseDeserializer):
    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_REGISTER:
            return cls._deserializer_from_register
        elif format_des == DES_ACCOUNT_MAIN_FROM_DB_FULL:
            return cls._deserializer_from_db_full
        elif format_des == DES_FROM_LOGIN:
            return cls._deserializer_from_login
        elif format_des == DES_FROM_RECOVERY_PASSWORD:
            return cls._deserializer_from_recovery_password
        else:
            raise TypeError

    @staticmethod
    def _deserializer_from_login(account_main_dict):
        return AccountMain(
            email=account_main_dict.get('email'),
            password=account_main_dict.get('password'),
            is_email_sent=account_main_dict.get('')
        )

    @staticmethod
    def _deserializer_from_register(account_main_dict):
        return AccountMain(
            name=account_main_dict.get('name'),
            password=account_main_dict.get('password'),
            email=account_main_dict.get('email')
        )

    @staticmethod
    def _deserializer_from_recovery_password(account_main_dict):
        return AccountMain(
            name=account_main_dict.get('name'),
            email=account_main_dict.get('email')
        )

    @staticmethod
    def _deserializer_from_db_full(account_main_record):
        return AccountMain(
            id=account_main_record.get('account_main_id'),
            created_at=account_main_record.get('account_main_created_at'),
            edited_at=account_main_record.get('account_main_edited_at'),
            email=account_main_record.get('account_main_email'),
            name=account_main_record.get('account_main_name'),
            hash_password=account_main_record.get('account_main_hash_password'),
            is_confirmed=account_main_record.get('account_main_is_confirmed')
        )
