from portfolio.internal.views.accounts import account
from portfolio.internal.views.main_api import main
from portfolio.internal.views.organisation import organisation
from portfolio.internal.views.parents import parents
from portfolio.internal.views.portfolio import portfolio
from portfolio.internal.views.private_office_parents import private_office_parents
from portfolio.internal.views.private_office_organisation import private_office_organisation

apis = [
    main,
    portfolio,
    account,
    parents,
    private_office_parents,
    organisation,
    private_office_organisation,
]
