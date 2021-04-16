import psycopg2
from psycopg2 import errorcodes
from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.account_main import AccountMainDeserializer, DES_ACCOUNT_MAIN_FROM_DB_FULL
from portfolio.models.account_main import AccountMain

UNIQUE_ACCOUNT_EMAIL = "unique_account_email"


class AccountMainDao(BaseDao):

    def add(self, account_main: AccountMain):
        sql = """
        INSERT INTO account_main(email, name, hash_password, is_confirmed) VALUES
        (%s, %s, %s, %s)
        RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(sql,
                                (account_main.email,
                                 account_main.name,
                                 account_main.hash_password,
                                 account_main.is_confirmed))
                    row = cur.fetchone()
                    cur.close()
                    conn.commit()
                except psycopg2.InternalError as err:
                    if err.pgcode == errorcodes.IN_FAILED_SQL_TRANSACTION:
                        conn.rollback()
                        return None, "RETURN"
                    else:
                        raise TypeError
                except psycopg2.IntegrityError as err:
                    if err.pgcode == errorcodes.UNIQUE_VIOLATION:
                        return None, "Not unique email"
                    else:
                        raise TypeError
            self.pool.putconn(conn)
        account_main.id = row[0]
        account_main.created_at = row[1]
        account_main.edited_at = row[2]

        return account_main, None

    def get_by_id(self, account_main_id: int):
        sql = """   SELECT
                        id              AS account_main_id,
                        created_at      AS account_main_created_at,
                        edited_at       AS account_main_edited_at,
                        email           AS account_main_email,
                        name            AS account_main_name,
                        hash_password   AS account_main_hash_password,
                        is_confirmed    AS account_main_is_confirmed,
                    FROM
                        account_main
                    WHERE
                        id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (account_main_id,))
                data = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if not data:
                return None, None

            return AccountMainDeserializer.deserialize(data, DES_ACCOUNT_MAIN_FROM_DB_FULL), None

    def get_by_email_and_name(self, account_main: AccountMain):
        sql = """   SELECT
                        id              AS account_main_id,
                        name            AS account_main_name,
                        email           AS account_main_email,
                        is_confirmed    AS account_main_is_confirmed
                    FROM
                        account_main
                    WHERE
                        email = %s AND name = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (account_main.email, account_main.name))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if row:
                return AccountMainDeserializer.deserialize(row, DES_ACCOUNT_MAIN_FROM_DB_FULL), None
            return None, None

    def get_by_email_and_hash_password(self, account_main: AccountMain):
        sql = """   SELECT 
                        id              AS account_main_id,
                        name            AS account_main_name,
                        email           AS account_main_email,
                        hash_password   AS account_main_hash_password,
                        is_confirmed    AS account_main_is_confirmed
                    FROM
                        account_main
                    WHERE
                        email = %s AND hash_password = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                print(account_main.hash_password)
                cur.execute(sql, (account_main.email, account_main.hash_password))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            print(row)
            if row:
                return AccountMainDeserializer.deserialize(row, DES_ACCOUNT_MAIN_FROM_DB_FULL), None
            return None, None

    def get_by_session_id(self, session_id):
        sql = """   SELECT
                        account_session.account_main_id AS account_main_id
                    FROM
                        account_session
                    WHERE 
                        id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (session_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if not row:
                return None, None
            print(row)
            return AccountMainDeserializer.deserialize(row, DES_ACCOUNT_MAIN_FROM_DB_FULL), None

    def get_by_session_id_with_confirmed(self, session_id: int):
        sql = """   SELECT
                        account_main.id             AS account_main_id,
                        account_main.is_confirmed   AS account_main_is_confirmed
                    FROM
                        account_main
                    INNER JOIN 
                        account_session ON account_main.id = account_session.account_main_id
                    WHERE account_session.id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (session_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if not row:
                return None, None
            return AccountMainDeserializer.deserialize(row, DES_ACCOUNT_MAIN_FROM_DB_FULL), None

    def get_email_by_id(self, auth_account_main_id: int):
        sql = """SELECT
                     email  AS account_main_email
                 FROM
                     account_main
                 WHERE
                     account_main.id = %s"""
        with self.pool.getconn() as conn:
            if self.conn:
                conn = self.conn
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (auth_account_main_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            account_email = row['account_main']
            if not account_email:
                return None, "Интересно..."

            return AccountMain(email=account_email), None

    def set_temp_psw(self, account_main: AccountMain):
        sql = """   UPDATE
                        account_main
                    SET
                        hash_password = %s
                    WHERE
                        id = %s
                    RETURNING id;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (account_main.hash_password, account_main.id))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
        if not row:
            return None, None
        return account_main, None
