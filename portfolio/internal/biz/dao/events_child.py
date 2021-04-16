from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.events_child import EventsChildDeserializer, \
    DES_FROM_DB_GET_INFO_CHILD_ORGANISATION
from portfolio.models.events_child import EventsChild
from portfolio.models.request_to_organisation import RequestToOrganisation


class EventsChildDao(BaseDao):

    def add_by_request(self, events_child: EventsChild):
        sql = """   INSERT INTO events_child(children_organisation_id, events_id) VALUES
                    (%s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(sql, (events_child.children_organisation.id,
                              events_child.events.id))
            row = cur.fetchone()
            cur.close()
        self.conn.commit()
        if not row:
            return None, "Я хз"
        events_child = EventsChild(
            id=row['id'],
            created_at=row['created_at'],
            edited_at=row['edited_at']
        )
        return events_child, None

    def update_status(self, events_child: EventsChild):
        sql = """   UPDATE
                        events_child
                    SET
                        status = true
                    WHERE
                        children_organisation_id = %s AND events_id = %s
                    RETURNING id;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (events_child.children_organisation.id,
                                  events_child.events.id))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "Ребенок не был добавлен в это событие"
        events_child.id = row['id']
        return events_child, None

    def get_by_child_organisation_id_or_child_id(self,
                                                 children_organisation_id: int = None,
                                                 children_id: int = None):
        sql = """   SELECT 
                        events_child.id                     AS events_child_id,
                        events_child.status                 AS events_child_status,
                        events.id                           AS events_id,
                        events.type                         AS events_type,
                        events.name                         AS events_name,
                        events.date_event                   AS events_date_event,
                        events.hours                        AS events_hours,
                        children_organisation.id            AS children_organisation_id,
                        children_organisation.children_id   AS children_id,
                        children.name                       AS children_name,
                        children.surname                    AS children_surname,
                        children.date_born                  AS children_date_born,
                        children.parents_id                 AS children_parents_id                        
                    FROM 
                        events_child
                    INNER JOIN
                        events ON events.id = events_child.events_id
                    INNER JOIN
                        children_organisation ON children_organisation.id = events_child.children_organisation_id
                    INNER JOIN 
                        children ON children.id = children_organisation.children_id
                    WHERE
                        (children_organisation.id = %s AND events_child.status = true) OR (children.id = %s AND events_child.status = true)"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                if children_organisation_id:
                    cur.execute(sql, (children_organisation_id,
                                      None))
                elif children_id:
                    cur.execute(sql, (None,
                                      children_id))
                else:
                    return None, 'Вы кто?'
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, "Ребенок не участовал в событиях"
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_INFO_CHILD_ORGANISATION), None
