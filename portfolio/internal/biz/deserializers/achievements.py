from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.achievements import Achievements
from portfolio.models.events import Events

DES_FROM_DB_GET_INFO_ACHIEVEMENTS = 'des-from-db-get-info-achievements'
DES_FROM_ADD_ACHIEVEMENT = 'des-from-add-achievement'


class AchievementsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_INFO_ACHIEVEMENTS:
            return cls._des_from_db_get_info_achievements
        elif format_des == DES_FROM_ADD_ACHIEVEMENT:
            return cls._des_from_add_achievement
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_info_achievements(row) -> Achievements:
        return Achievements(
            id=row['achievements_id'],
            events=Events(
                id=row['achievements_events_id']
            ),
            name=row['achievements_name'],
            point=row['achievements_point'],
            nomination=row['achievements_nomination'],
        )

    @staticmethod
    def _des_from_add_achievement(dict_achiev) -> Achievements:
        return Achievements(
            id=dict_achiev.get('id'),
            name=dict_achiev.get('name'),
            point=dict_achiev.get('point'),
            nomination=dict_achiev.get('nomination')
        )
