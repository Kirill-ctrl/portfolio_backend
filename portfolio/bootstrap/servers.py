from portfolio.configs.http_server import HOST, PORT, DEBUG
from portfolio.drivers.flask_server import FlaskServer
from portfolio.internal.views.blueprint_api import apis


def init_http_server():
    FlaskServer.set_api(apis)


def run_http_server():
    FlaskServer.run_server(HOST, PORT, DEBUG)
