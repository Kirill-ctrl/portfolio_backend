from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.achievements import Achievements

SER_FOR_ADD_ACHIEVEMENT = 'ser-for-add-achievement'
SER_FOR_DETAIL_ACHIEVEMENTS_CHILD = 'ser-for-detail-achievements_child'


class AchievementsSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_ADD_ACHIEVEMENT:
            return cls._ser_for_add_achievement
        elif format_ser == SER_FOR_DETAIL_ACHIEVEMENTS_CHILD:
            return cls._ser_for_detail_achievements_child
        else:
            raise TypeError

    @staticmethod
    def _ser_for_add_achievement(achievements: Achievements):
        return {
            'id': achievements.id,
            'created_at': achievements.created_at,
            'edited_at': achievements.edited_at
        }

    @staticmethod
    def _ser_for_detail_achievements_child(achievements: Achievements):
        return {
            'event': {
                'id': achievements.events.id
            },
            'id': achievements.id,
            'name': achievements.name,
            'point': achievements.point,
            'nomination': achievements.nomination
        }
