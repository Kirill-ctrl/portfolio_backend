from psycopg2 import extras

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.achievements import Achievements


class AchievementsDao(BaseDao):

    def add(self, achievement: Achievements):
        sql = """   INSERT INTO achievements(events_id, name, point, nomination) VALUES
                    (%s, %s, %s, %s)
                    RETURNING id, created_at, edited_at;"""
        with self.pool.getconn() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(sql, (achievement.events.id,
                                  achievement.name,
                                  achievement.point,
                                  achievement.nomination))
                row = cur.fetchone()
                cur.close()
            self.pool.putconn(conn)
        if not row:
            return None, "Я вообще ничего не понимаю"
        achievement.id = row['id']
        achievement.created_at = row['created_at'],
        achievement.edited_at = row['edited_at']
        return achievement, None
