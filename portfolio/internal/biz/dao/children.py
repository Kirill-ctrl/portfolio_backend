from typing import List, Optional, Tuple

from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FROM_DB_INFO_CHILD, \
    DES_FROM_DB_ALL_CHILDREN, DES_FROM_DB_INFO_CHILD_WITH_PARENTS, DES_FROM_DB_INFO_CHILDREN
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

    def get_by_parents_id(self, children: Children):
        sql = """   SELECT 
                        children.id         AS children_id,
                        children.name       AS children_name,
                        children.surname    AS children_surname,
                        children.date_born  AS children_date_born,
                        parents.id          AS parents_id,
                        parents.name        AS parents_name,
                        parents.surname     AS parents_surname
                    FROM
                        children
                    INNER JOIN 
                        parents ON parents.id = children.parents_id
                    WHERE
                        parents.id = %s AND children.name = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (children.parents.id, children.name))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if not row:
                return None, "Сначала добавьте ребенка"
            return ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILD), None

    def get_all_by_parents_id(self, children: Children):
        sql = """   SELECT
                        id          AS children_id,
                        name        AS children_name,
                        surname     AS children_surname,
                        date_born   AS children_date_born,
                        parents_id  AS parents_id
                    FROM 
                        children
                    WHERE
                        children.parents_id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (children.parents.id,))
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, "Сначала добавьте детей"
        return ChildrenDeserialize.deserialize(data, DES_FROM_DB_ALL_CHILDREN), None

    def get_by_request_id(self, request_id):
        sql = """   SELECT
                        id                          AS children_id,
                        name                        AS children_name,
                        surname                     AS children_surname,
                        date_born                   AS children_date_born,
                        parents_id                  AS children_parents_id,
                        parents.account_main_id     AS parents_account_main_id
                    FROM
                        children
                    INNER JOIN 
                        parents ON parents.id = children.id
                    INNER JOIN
                        request_to_organisation ON request_to_organisation.parents_id = partners.id
                    WHERE
                        request_id = %s"""
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(sql, (request_id,))
            row = cur.fetchone()
            cur.close()
        if not row:
            return None, "Такого запроса не существует"
        return ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILD_WITH_PARENTS), None

    def get_list_by_tuple_children_id(self, tuple_children_id) -> Tuple[Optional[List[Children]], Optional[None]]:
        sql = """   SELECT
                        children.id                 AS children_id,
                        children.name               AS children_name,
                        children.surname            AS children_surname,
                        children.date_born          AS children_date_born
                    FROM
                        children
                    WHERE
                        children.id IN %s
                    ORDER BY 
                        children.id"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (tuple_children_id,))
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        return [ChildrenDeserialize.deserialize(data[i], DES_FROM_DB_INFO_CHILDREN) for i in range(len(data))], None
