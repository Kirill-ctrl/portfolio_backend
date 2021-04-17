from datetime import datetime

from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.events import EventDeserializer, DES_FROM_DB_FULL_EVENTS_BY_ORG_ID, \
    DES_FROM_DB_GET_DETAIL_EVENT
from portfolio.models.events import Events


class EventsDao(BaseDao):

    def add(self, event: Events):
        sql = """   INSERT INTO events(type, name, date_event, hours, skill, organisation_id) VALUES
                    (%s, %s, %s, %s, %s,%s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (event.type, event.name, event.date_event, event.hours, event.skill,event.organisation.id))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
        event.id = row['id']
        event.created_at = row['created_at']
        event.edited_at = row['edited_at']
        return event, None

    def get_by_organisation_id(self, organisation_id: int):
        sql = """   SELECT 
                        id                  AS events_id,
                        type                AS events_type,
                        name                AS events_name,
                        date_event          AS events_date_event,
                        hours               AS events_hours,
                        skill               AS events_skill,
                        organisation_id     AS events_organisation_id
                    FROM
                        events
                    WHERE
                        organisation_id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (organisation_id,))
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, "У этой организации нет событий"
        return EventDeserializer.deserialize(data, DES_FROM_DB_FULL_EVENTS_BY_ORG_ID), None

    def get_by_id(self, event_id: int):
        sql = """   SELECT 
                        id                  AS events_id,
                        type                AS events_type,
                        name                AS events_name,
                        date_event          AS events_date_event,
                        hours               AS events_hours,
                        skill               AS events_skill,
                        organisation_id     AS events_organisation_id
                    FROM
                        events
                    WHERE
                        id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (event_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "Данное событие не существует"
        return EventDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_EVENT), None

    def get_focus_by_sort_date(self, result_sort_focus: datetime.date, children_id: int):
        sql = """   SELECT
                        SUM(events.hours)   AS sum_events_hours,
                        events.skill        AS events_skill
                    FROM
                        events
                    INNER JOIN 
                        events_child ON events_child.events_id = events.id
                    INNER JOIN
                        children_organisation ON children_organisation.id = events_child.children_organisation_id
                    WHERE
                        children_organisation.children_id = %s AND events_child.status = true AND events.date_event > %s
                    GROUP BY
                        events.skill
                    ORDER BY
                        sum_events_hours DESC;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (children_id,
                                  result_sort_focus))
                row = cur.fetchone()[0]
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "Статистики нет"
        return {
            'skill': row['events_skill'],
            'focus_hours': row['sum_events_hours']
        }

    def get_id_by_name(self, events_name: str):
        sql = """   SELECT 
                        id   AS events_id
                    FROM
                        events
                    WHERE
                        events.name = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (events_name,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "События с таким именем не существует"
        return Events(id=row['events_id']), None
