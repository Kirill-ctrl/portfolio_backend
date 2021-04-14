from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.auth_code import AuthCodeDeserializer, DES_AUTH_CODE_FROM_DB_FULL
from portfolio.models.auth_code import AuthCode


class AuthCodeDao(BaseDao):

    def add(self, auth_code: AuthCode):
        sql = """
        INSERT INTO auth_code(account_main_id, code) VALUES
        (%s, %s);
        """
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (auth_code.account_main.id, auth_code.code))
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
        return auth_code, None

    def update(self, auth_code_id: int, auth_code: AuthCode):
        sql = """   UPDATE
                        auth_code
                    SET
                        edited_at = CURRENT_TIMESTAMP
                        code = %s
                    WHERE
                        auth_code.id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (auth_code.code, auth_code_id))
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
        return auth_code, None

    def get_code_by_account_main_id(self, auth_code: AuthCode):
        sql = """SELECT
                    id,
                    edited_at
                 FROM
                     auth_code
                 WHERE
                     account_main_id = %s AND code = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (auth_code.account_main.id, auth_code.code))
                row = cur.fetchone()
                cur.close()
                if not row:
                    return None, None
            self.pool.putconn(conn)
        auth_code.id = row[0]
        auth_code.edited_at = row[1]

        return auth_code, None

    def set_is_confirm(self, account_main_id: int, is_confirmed: bool):
        sql = """   UPDATE account_main
                    SET
                        is_confirmed = %s
                    WHERE
                        account_main.id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (is_confirmed, account_main_id))
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            return None, None

    def remove_by_id(self, auth_code_id: int):
        sql = """   DELETE
                    FROM 
                        auth_code
                    WHERE 
                        id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (auth_code_id,))
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            return None, None

    def get_by_account_main_id(self, auth_account_main_id: int):
        sql = """   SELECT
                        id AS auth_code_id,
                        edited_at AS auth_code_edited_at
                    FROM
                        auth_code
                    WHERE
                        account_main_id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (auth_account_main_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if not row:
                return None, None
            return AuthCodeDeserializer.deserialize(row, DES_AUTH_CODE_FROM_DB_FULL), None
