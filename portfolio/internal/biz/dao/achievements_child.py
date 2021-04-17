from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.achievements_child import AchievementsChildDeserializer, \
    DES_FROM_DB_GET_ALL_ACHIV_BY_CHILD


class AchievementsChildDao(BaseDao):

    def get_by_children_organisation_id_or_child_id(self,
                                                    children_organisation_id: int = None,
                                                    children_id: int = None):
        sql = """   SELECT 
                        achievements_child.id   AS achievements_child_id,
                        achievements.id         AS achievements_id,
                        achievements.events_id  AS achievements_events_id,
                        achievements.name       AS achievements_name,
                        achievements.point      AS achievements_point,
                        achievements.nomination AS achievements_nomination
                    FROM
                        achievements_child
                    INNER JOIN
                        achievements ON achievements.id = achievements_child.achievements_id
                    INNER JOIN
                        children_organisation ON achievements_child.children_organisation_id = children_organisation.id
                    WHERE
                        (achievements_child.children_organisation_id = %s) OR (children_organisation.children_id = %s)"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                if children_organisation_id:
                    cur.execute(sql, (children_organisation_id,
                                      -1))
                elif children_id:
                    cur.execute(sql, (-1,
                                      children_id))
                else:
                    return None, 'Вы кто?'
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, None
        return AchievementsChildDeserializer.deserialize(data, DES_FROM_DB_GET_ALL_ACHIV_BY_CHILD), None
