from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.account_session import AccountSession


class AccountSessionDao(BaseDao):

    def add(self, account_session: AccountSession):
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO account_session(account_main_id) VALUES (%s)
                    RETURNING id;
                """
                cur.execute(sql, (account_session.account_main.id,))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
        account_session.id = row[0]
        return account_session, None
