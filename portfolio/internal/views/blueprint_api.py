from portfolio.internal.views.accounts import account
from portfolio.internal.views.main_api import main
from portfolio.internal.views.parents import parents
from portfolio.internal.views.portfolio import portfolio

apis = [
    main,
    portfolio,
    account,
    parents,
]
