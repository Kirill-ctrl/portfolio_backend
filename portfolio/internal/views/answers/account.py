from portfolio.internal.biz.serializers.account_main import AccountMainSerializer, SER_FOR_REGISTER, SER_FOR_DETAIL, \
    SER_FOR_RECOVERY_PASSWORD, SER_FOR_LOGIN
from portfolio.models.account_main import AccountMain


def get_response_register(account_main: AccountMain):
    return AccountMainSerializer.serialize(account_main, SER_FOR_REGISTER)


def get_response_account_detail(account_main: AccountMain):
    return AccountMainSerializer.serialize(account_main, SER_FOR_DETAIL)


def get_response_login(account_main: AccountMain):
    return AccountMainSerializer.serialize(account_main, SER_FOR_LOGIN)


def get_response_recovery_password(account_main: AccountMain):
    return AccountMainSerializer.serialize(account_main, SER_FOR_RECOVERY_PASSWORD)