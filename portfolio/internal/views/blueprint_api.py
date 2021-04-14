from portfolio.internal.views.accounts import account
from portfolio.internal.views.main_api import main
from portfolio.internal.views.parents import parents
from portfolio.internal.views.portfolio import portfolio
from portfolio.internal.views.private_office import private_office

apis = [
    main,
    portfolio,
    account,
    parents,
    private_office,
]
