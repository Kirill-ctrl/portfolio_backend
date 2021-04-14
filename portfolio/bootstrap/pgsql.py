from portfolio.configs.pgsql import HOST, USER, PASSWORD, PORT, DB_NAME
from portfolio.drivers.pg_server import Pg


def init_pgsql_server():
    Pg.init_db(HOST, USER, PASSWORD, PORT, DB_NAME)
