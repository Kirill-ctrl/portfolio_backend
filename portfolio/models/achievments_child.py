from datetime import datetime
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.achievements import Achievements
from portfolio.models.children_organisation import ChildrenOrganisation


class AchievementsChild(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 children_organisation: Optional[ChildrenOrganisation] = None,
                 achievements: Optional[Achievements] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__children_organisation = children_organisation
        self.__achievements = achievements

    @property
    def children_organisation(self):
        return self.__children_organisation

    @property
    def achievements(self):
        return self.__achievements

    @children_organisation.setter
    def children_organisation(self, value: ChildrenOrganisation):
        self.__children_organisation = value

    @achievements.setter
    def achievements(self, value: Achievements):
        self.__achievements = value
