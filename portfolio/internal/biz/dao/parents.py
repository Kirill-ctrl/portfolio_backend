from psycopg2 import extras, sql

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.parents import Parents


class ParentsDao(BaseDao):

    def add(self, parents: Parents):
        sql = """   INSERT INTO parents(name, surname, account_main_id) VALUES
                    (%s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (parents.name, parents.surname, parents.account_main.id))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            parents.id = row['id']
            parents.created_at = row['created_at']
            parents.edited_at = ['edited_at']
            return parents, None

    def update(self, account_main_id, parents: Parents):
        query = sql.SQL("""
                    UPDATE
                        parents
                    SET
                        name = CASE WHEN {name_field}::varchar != '-1' THEN {name_field}::varchar WHEN {name_field}::varchar = '-1' THEN name END,
                        surname = CASE WHEN {surname_field}::varchar != '-1' THEN {surname_field}::varchar WHEN {surname_field}::varchar = '-1' THEN surname END,
                        edited_at = current_timestamp
                    WHERE 
                        account_main_id = {account_main_id}
                    RETURNING id, edited_at;""").format(name_field=sql.Identifier(parents.name),
                                             surname_field=sql.Identifier(parents.surname),
                                             account_main_id=sql.Identifier(parents.account_main.id))
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query)
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            parents.id = row['id']
            parents.edited_at = row['edited_at']
            return parents, None
