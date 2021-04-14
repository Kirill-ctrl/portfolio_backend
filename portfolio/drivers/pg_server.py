import psycopg2
from psycopg2 import pool


class Pg:

    __connection = None
    __cursor = None
    __pool_db = None

    @classmethod
    def get_pool_db(cls):
        return cls.__pool_db

    @classmethod
    def get_connection_db(cls):
        return cls.__connection

    @classmethod
    def get_cursor_db(cls):
        return cls.__cursor

    # @classmethod
    # def init_db(cls, host: str, user: str, password: str, port: int, database: str):
    #     cls.__connection = connect(f"dbname={database} user={user} password='{password}' host={host} port={port}")
    #     cls.__cursor = cls.__connection.cursor()

    @classmethod
    def init_db(cls, host: str, user: str, password: str, port: int, database: str):
        cls.__pool_db = psycopg2.pool.SimpleConnectionPool(1,
                                                           20,
                                                           user=user,
                                                           password=password,
                                                           host=host,
                                                           port=port,
                                                           database=database)
