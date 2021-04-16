from portfolio.internal.biz.dao.achievements import AchievementsDao
from portfolio.models.achievements import Achievements


class AchievementService:

    @staticmethod
    def add_achievement(achievement: Achievements):
        achievement, err = AchievementsDao().add(achievement)
        if err:
            return None, err

        return achievement, None
