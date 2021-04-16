from datetime import datetime

from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.children_organisation import ChildrenOrganisationDeserializer, \
    DES_FROM_DB_GET_ALL_LEARNERS
from portfolio.models.children_organisation import ChildrenOrganisation


class ChildrenOrganisationDao(BaseDao):

    def add(self, children_organisation: ChildrenOrganisation):
        sql = """   INSERT INTO children_organisation(teacher_id, children_id) VALUES
                    (%s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(sql, (children_organisation.teacher.id, children_organisation.children.id))
            row = cur.fetchone()
            cur.close()
            self.conn.commit()
        children_organisation.id = row['id']
        children_organisation.created_at = row['created_at']
        children_organisation.edited_at = row['edited_at']
        return children_organisation, None

    def get_all_by_organisation_id(self, organisation_id: int):
        sql = """   SELECT 
                        id                  AS children_organisation_id,
                        teacher_id          AS children_organisation_teacher_id,
                        children_id         AS children_id,
                        children.name       AS children_name,
                        children.surname    AS children_surname,
                        children.date_born  AS children_date_born
                    FROM
                        children_organisation
                    INNER JOIN
                        children ON children.id = children_organisation.children_id
                    INNER JOIN
                        teacher ON teacher.id = children_organisation.teacher_id
                    WHERE teacher.organisation_id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (organisation_id,))
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, "У вас нет обучающихся"
        return ChildrenOrganisationDeserializer.deserialize(data, DES_FROM_DB_GET_ALL_LEARNERS), None

    def get_statistic_by_sort_date(self, result_sort_statistic: datetime.date, children_id: int):
        sql = """   SELECT
                        SUM(events.hours)   AS      sum_hours,
                        events.skill        AS      events_skill
                    FROM
                        children_organisation
                    INNER JOIN
                        events_child ON events_child.children_organisation_id = children_organisation.id
                    INNER JOIN
                        events ON events_child.events_id = events.id
                    WHERE
                        events_child.status = true AND children_organisation.children_id = %s AND events.date_event > %s
                    GROUP BY
                        events.skill 
                    ORDER BY
                        sum_hours"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (children_id,
                                  result_sort_statistic))
                data = cur.fetchall()
            self.pool.putconn(conn)
        if not data:
            return None, 'Статистики нет'
        return {
            'skills': {
                'skill': data[i]['events_skill'],
                'sum_hours': data[i]['sum_hours']
            }
            for i in range(len(data))
        }
