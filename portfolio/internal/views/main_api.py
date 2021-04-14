from flask import Blueprint, request, url_for, redirect

main = Blueprint('main', __name__, template_folder='templates/main', static_folder='static/main')


@main.route('', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        return 'hello world'
