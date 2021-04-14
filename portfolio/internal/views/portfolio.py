from flask import Blueprint, request

from portfolio.internal.middlewares.auth import required_auth_with_confirmed_email

portfolio = Blueprint('portfolio', __name__, template_folder="templates/portfolio", static_folder='static/portfolio')


@portfolio.route('/add_child', methods=['GET', 'POST'])
@required_auth_with_confirmed_email
def add_child(auth_account_main_id):
    if request.method == 'POST':
        pass