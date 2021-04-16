from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.events import EventDeserializer, DES_FROM_DB_FULL_EVENTS_BY_ORG_ID, \
    DES_FROM_DB_GET_DETAIL_EVENT
from portfolio.models.events import Events


class EventsDao(BaseDao):

    def add(self, event: Events):
        sql = """   INSERT INTO events(type, name, date_event, hours, organisation_id) VALUES
                    (%s, %s, %s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (event.type, event.name, event.date_event, event.hours, event.organisation.id))
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
                        id                  AS events_id
                        type                AS events_type,
                        name                AS events_name,
                        date_event          AS events_date_event,
                        hours               AS events_hours,
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
        return EventDeserializer.deserialize(data, DES_FROM_DB_FULL_EVENTS_BY_ORG_ID)

    def get_by_id(self, event_id: int):
        sql = """   SELECT 
                        id                  AS events_id
                        type                AS events_type,
                        name                AS events_name,
                        date_event          AS events_date_event,
                        hours               AS events_hours,
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
        return EventDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_EVENT)
