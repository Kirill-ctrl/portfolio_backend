from datetime import datetime

import psycopg2
from psycopg2 import extras, errorcodes, sql

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.organisation import OrganisationDeserializer, DES_FROM_DB_FULL_ORGANISATION, \
    DES_FROM_DB_GET_ORGANISATION
from portfolio.internal.biz.deserializers.teacher import TeacherDeserializer, DES_FROM_DB_DETAIL_TEACHER
from portfolio.models.account_main import AccountMain
from portfolio.models.organisation import Organisation


class OrganisationDao(BaseDao):

    def add(self, organisation: Organisation):
        sql = """   INSERT INTO organisation(account_main_id, name, login, photo_link, description) VALUES
                    (%s, %s, %s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                try:
                    cur.execute(sql, (organisation.account_main.id,
                                      organisation.name,
                                      organisation.login,
                                      organisation.photo_link,
                                      organisation.description))
                    row = cur.fetchone()
                    cur.close()
                    conn.commit()
                except psycopg2.IntegrityError as err:
                    if err.pgcode == errorcodes.UNIQUE_VIOLATION:
                        return None, "Эта организация уже зарегистрирована"
                    else:
                        raise TypeError
            self.pool.putconn(conn)
        organisation.id = row['id']
        organisation.created_at = row['created_at']
        organisation.edited_at = row['edited_at']
        return organisation, None

    def update(self, account_main_id, organisation: Organisation):
        query = sql.SQL("""   UPDATE
                        organisation
                    SET
                        name = CASE WHEN {name_field}::varchar != '-1' THEN {name_field}::varchar WHEN {name_field}::varchar = '-1' THEN name END,
                        login = CASE WHEN {login_field}::varchar != '-1' THEN {login_field}::varchar WHEN {login_field}::varchar = '-1' THEN login END,
                        photo_link = CASE WHEN {photo_link_field}::varchar != '-1' THEN {photo_link_field}::varchar WHEN {photo_link_field}::varchar = '-1' THEN photo_link END,
                        description = CASE WHEN {description_field}::varchar != '-1' THEN {description_field}::varchar WHEN {description_field}::varchar = '-1' THEN description END,
                        edited_at = current_timestamp
                    WHERE 
                        account_main_id = {account_main_id}
                    RETURNING id, edited_at;""").format(name_field=sql.Identifier(organisation.name),
                                                        login_field=sql.Identifier(organisation.login),
                                                        photo_link_field=sql.Identifier(organisation.photo_link),
                                                        description_field=sql.Identifier(organisation.description),
                                                        account_main_id=sql.Identifier(organisation.account_main.id))
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query)
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            organisation.id = row['id']
            organisation.edited_at = row['edited_at']
            return organisation, None

    def remove(self, organisations: Organisation):
        sql = """   DELETE FROM 
                        organisation
                    WHERE 
                        account_main_id = %s
                    RETURNING id;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (organisations.account_main.id,))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            organisations.id = row['id']
            return organisations, None

    def get_by_id(self, account_main_id: int):
        sql = """   SELECT 
                        id              AS organisation_id,
                        name            AS organisation_name,
                        login           AS organisation_login, 
                        account_main_id AS account_main_id
                    FROM 
                        organisation
                    WHERE   
                        account_main_id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (account_main_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
            if not row:
                return None, "Сначала зарегистрируйте себя как организацию"
            organisation = Organisation(
                id=row['organisation_id'],
                name=row['organisation_name'],
                login=row['organisation_login'],
                account_main=AccountMain(id=row['account_main_id'])
            )
            return organisation, None

    def get_all_by_account_id(self, account_main_id):
        sql = """   SELECT 
                        organisation.id             AS organisation_id,
                        organisation.created_at     AS organisation_created_at,
                        organisation.name           AS organisation_name,
                        organisation.photo_link     AS organisation_photo_link,
                        organisation.description    AS organisation_description,
                        teacher.name                AS teacher_name,
                        teacher.surname             AS teacher_surname,
                        teacher.specialty           AS teacher_specialty
                    FROM
                        organisation
                    INNER JOIN
                        teacher ON teacher.organisation_id = organisation.id
                    WHERE 
                        account_main_id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (account_main_id,))
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, "Учителей нет"
        return TeacherDeserializer.deserialize(data, DES_FROM_DB_DETAIL_TEACHER), None

    def get_all(self):
        sql = """   SElECT
                        id              AS organisation_id,
                        name            AS organisation_name,
                        login           AS organisation_login,
                        photo_link      AS organisation_photo_link,
                        description     AS organisation_description
                    FROM
                        organisation"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
            self.pool.putconn(conn)
        if not data:
            return None, "Нет зарегистрированных компаний"
        return OrganisationDeserializer.deserialize(data, DES_FROM_DB_FULL_ORGANISATION), None

    def get_by_org_id(self, organisation_id: int):
        sql = """   SELECT 
                        id              AS organisation_id,
                        name            AS organisation_name,
                        login           AS organisation_login,
                        photo_link      AS organisation_photo_link,
                        description     AS organisation_description
                    FROM
                        organisation
                    WHERE
                        organisation.id = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (organisation_id,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "Такой компании не существует"
        return OrganisationDeserializer.deserialize(row, DES_FROM_DB_GET_ORGANISATION)

    def get_id_by_org_name(self, organisation_name: str):
        sql = """   SELECT 
                        id              AS organisation_id
                    FROM
                        organisation
                    WHERE
                        organisation.name = %s"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (organisation_name,))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "Такой компании не существует"
        return Organisation(id=row['organisation_id']), None
