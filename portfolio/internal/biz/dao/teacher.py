from psycopg2 import extras, sql

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.teacher import Teacher


class TeacherDao(BaseDao):

    def add(self, teacher: Teacher):
        sql = """   INSERT INTO teacher(name, surname, organisation_id, specialty) VALUES
                    (%s, %s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (teacher.name, teacher.surname, teacher.organisation.id, teacher.specialty))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            teacher.id = row['id']
            teacher.created_at = row['created_at']
            teacher.edited_at = row['edited_at']
            return teacher, None

    def update(self, organisation_id: int, teacher: Teacher):
        query = sql.SQL("""
                            UPDATE
                                parents
                            SET
                                name = CASE WHEN {name_field}::varchar != '-1' THEN {name_field}::varchar WHEN {name_field}::varchar = '-1' THEN name END,
                                surname = CASE WHEN {surname_field}::varchar != '-1' THEN {surname_field}::varchar WHEN {surname_field}::varchar = '-1' THEN surname END,
                                specialty = CASE WHEN {specialty_field}::varchar != '-1' THEN {specialty_field}::varchar WHEN {specialty_field}::varchar = '-1' THEN specialty END,
                                edited_at = current_timestamp
                            WHERE 
                                account_main_id = {account_main_id}
                            RETURNING id, edited_at;""").format(name_field=sql.Identifier(teacher.name),
                                                                surname_field=sql.Identifier(teacher.surname),
                                                                organisation_id=sql.Identifier(teacher.organisation.id))
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query)
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            teacher.id = row['id']
            teacher.edited_at = row['edited_at']
            return teacher, None

    def remove(self, teacher: Teacher):
        sql = """
                    DELETE FROM 
                        teacher
                    WHERE 
                        organisation_id = %s
                    RETURNING id;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (teacher.organisation.id,))
                row = cur.fetchone()
                cur.close()
                conn.commit()
            self.pool.putconn(conn)
            teacher.id = row['id']
            return teacher, None

    def get_id_by_organisation_id(self, teacher: Teacher):
        sql = """   SELECT
                        id          AS teacher_id
                    FROM
                        teacher
                    WHERE 
                        organisation_id = %s AND name = %s AND surname = %s;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (teacher.organisation.id, teacher.name, teacher.surname))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, 'Учитель с таким именем на закреплен за вашей организацией'
        teacher.id = row['teacher_id']
        return teacher, None
