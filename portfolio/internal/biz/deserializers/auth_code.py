from portfolio.internal.biz.deserializers.account_main import AccountMainDeserializer, DES_ACCOUNT_MAIN_FROM_DB_FULL
from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.utils import filter_keys_by_substr
from portfolio.models.auth_code import AuthCode

DES_AUTH_CODE_FROM_DB_FULL = 'des-auth-code-from-db-full'


class AuthCodeDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_AUTH_CODE_FROM_DB_FULL:
            return cls._deserializer_from_db_full
        else:
            raise TypeError

    @staticmethod
    def _deserializer_from_db_full(auth_code):
        account_main_dict = filter_keys_by_substr(auth_code, 'account_main')
        return AuthCode(
            id=auth_code.get('auth_code_id'),
            created_at=auth_code.get('auth_code_created_at'),
            edited_at=auth_code.get('auth_code_edited_at'),
            account_main=AccountMainDeserializer.deserialize(account_main_dict, DES_ACCOUNT_MAIN_FROM_DB_FULL),
            code=auth_code.get('auth_code_code')
        )
