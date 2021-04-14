from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.children import Children


class ChildrenDao(BaseDao):

    def add(self, children: Children):
        sql = """   INSERT INTO children(parents_id, name, surname, date_born) VALUES
                    (%s, %s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (children.parents.id, children.name, children.surname, children.date_born))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            if not row:
                return None, "Как же так"
            children.id = row['id']
            children.created_at = row['created_at']
            children.edited_at = row['edited_at']
            return children, None
