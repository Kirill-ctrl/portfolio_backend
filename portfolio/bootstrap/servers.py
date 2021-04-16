from portfolio.configs.http_server import HOST, PORT, DEBUG, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from portfolio.drivers.flask_server import FlaskServer
from portfolio.internal.views.blueprint_api import apis


def init_http_server():
    FlaskServer.set_api(apis)
    FlaskServer.set_config(UPLOAD_FOLDER, MAX_CONTENT_LENGTH)


def run_http_server():
    FlaskServer.run_server(HOST, PORT, DEBUG)
