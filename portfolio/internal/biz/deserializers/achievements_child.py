from typing import List

from portfolio.internal.biz.deserializers.achievements import AchievementsDeserializer, \
    DES_FROM_DB_GET_INFO_ACHIEVEMENTS
from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.achievments_child import AchievementsChild

DES_FROM_DB_GET_ALL_ACHIV_BY_CHILD = 'des-from-db-get-all-achiv-by-child'


class AchievementsChildDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_ALL_ACHIV_BY_CHILD:
            return cls._des_from_db_get_all_achiv_by_child
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_all_achiv_by_child(data) -> List[AchievementsChild]:
        return [
            AchievementsChild(
                id=data[i]['achievements_child_id'],
                achievements=AchievementsDeserializer.deserialize(data[i], DES_FROM_DB_GET_INFO_ACHIEVEMENTS)
            )
            for i in range(len(data))
        ]
