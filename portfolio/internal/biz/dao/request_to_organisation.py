from typing import Optional, Tuple

import psycopg2
from psycopg2 import extras

from portfolio.internal.biz.dao.account_main import AccountMainDao
from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.dao.children import ChildrenDao
from portfolio.internal.biz.dao.children_organisation import ChildrenOrganisationDao
from portfolio.internal.biz.dao.events_child import EventsChildDao
from portfolio.internal.biz.deserializers.request_to_deserializer import RequestToOrganisationDeserializer, \
    DES_FROM_DB_GET_LIST_REQUESTS
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events import Events
from portfolio.models.events_child import EventsChild
from portfolio.models.request_to_organisation import RequestToOrganisation


class RequestToOrganisationDao(BaseDao):

    def add(self, request_to_organisation: RequestToOrganisation):
        sql = """   INSERT INTO request_to_organisation(parents_id, events_id, children_id)
                    VALUES(%s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (request_to_organisation.parents.id,
                                  request_to_organisation.events.id,
                                  request_to_organisation.children.id))
                row = cur.fetchone()
                cur.close()
            conn.commit()
            self.pool.putconn(conn)
        if not row:
            return None, "МДААААА"
        request_to_organisation.id = row['id']
        request_to_organisation.created_at = row['created_at']
        request_to_organisation.edited_at = row['edited_at']
        return request_to_organisation, None

    def get_all_request_by_org_id(self, request_to_organisation: RequestToOrganisation):
        sql = """   SELECT
                        events.organisation_id              AS events_organisation_id,
                        request_to_organisation.id          AS request_id,
                        request_to_organisation.children_id AS request_children_id,
                        request_to_organisation.status      AS request_status,
                        events.id                           AS events_id,
                        events.name                         AS events_name,
                        events.date_event                   AS events_date_event,
                        parents.id                          AS parents_id,
                        parents.name                        AS parents_name,
                        parents.surname                     AS parents_surname
                    FROM
                        request_to_organisation
                    INNER JOIN 
                        events ON request_to_organisation.events_id = events.id
                    INNER JOIN
                        parents ON request_to_organisation.parents_id = parents.id
                    WHERE
                        events.organisation_id = %s
                    ORDER BY 
                        request_to_organisation.children_id
                    """
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (request_to_organisation.events.organisation.id,))
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
            if not data:
                return None, "Нет активных запросов"
        return RequestToOrganisationDeserializer.deserialize(data, DES_FROM_DB_GET_LIST_REQUESTS), None

    def get_event_id(self, request_to_organisation: RequestToOrganisation):
        sql = """   SELECT
                        events_id   AS events_id
                    FROM 
                        request_to_organisation
                    WHERE
                        id = %s;"""
        cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(sql, (request_to_organisation.id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return None, "Такого события не существует"
        request_to_organisation.events = Events(id=row['events_id'])
        return request_to_organisation, None

    def update_status(self, request_to_organisation: RequestToOrganisation):
        sql = """   UPDATE
                        request_to_organisation
                    SET status = true
                    WHERE
                        id = %s
                    RETURNING status;"""
        cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(sql, (request_to_organisation.id,))
        row = cur.fetchone()
        cur.close()
        self.conn.commit()
        if not row['status']:
            return None, "хммммм"
        request_to_organisation.status = row['status']
        return request_to_organisation, None

    def accept_request(self, request_to_organisation: RequestToOrganisation) -> Tuple[Optional[RequestToOrganisation], Optional[str or None]]:
        conn = self.simple_connection
        try:
            request_to_organisation, err = RequestToOrganisationDao(conn).get_event_id(request_to_organisation)
            if err:
                return None, err

            children, err = ChildrenDao(conn).get_by_request_id(request_to_organisation.id)
            if err:
                return None, err

            request_to_organisation.children = children

            parents_account_main, err = AccountMainDao(conn).get_email_by_id_into_transaction(children.parents.account_main.id)
            if err:
                return None, err

            request_to_organisation.children.parents.account_main = parents_account_main

            children_organisation = ChildrenOrganisation(children=request_to_organisation.children,
                                                         teacher=None)

            # TODO ДОБАВИТЬ TEACHER_ID
            children_organisation, err = ChildrenOrganisationDao(conn).add(children_organisation)
            if err:
                return None, err

            events_child = EventsChild(events=Events(
                id=request_to_organisation.events.id

            ),
                children_organisation=ChildrenOrganisation(
                    id=children_organisation.id,
                )
            )

            events_child, err = EventsChildDao(conn).add_by_request(events_child)
            if err:
                return None, err

            request_to_organisation, err = RequestToOrganisationDao(conn).update_status(request_to_organisation)
            if err:
                return None, err

            return request_to_organisation, None
        except (Exception, psycopg2.DatabaseError) as error :
            conn.roolback()
            raise error
        finally:
            conn.close()
