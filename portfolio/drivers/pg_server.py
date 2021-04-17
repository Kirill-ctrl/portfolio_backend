import psycopg2
from psycopg2 import pool


class Pg:

    __pool_db = None
    __dsn = None

    @classmethod
    def get_pool_db(cls):
        return cls.__pool_db

    @classmethod
    def get_connection_db(cls):
        return psycopg2.connect(cls.__dsn)

    @classmethod
    def init_db(cls, host: str, user: str, password: str, port: int, database: str):
        cls.__dsn = f'user={user} password={password} host={host} port={port} dbname={database}'
        cls.__pool_db = psycopg2.pool.SimpleConnectionPool(1,
                                                           20,
                                                           user=user,
                                                           password=password,
                                                           host=host,
                                                           port=port,
                                                           database=database)
