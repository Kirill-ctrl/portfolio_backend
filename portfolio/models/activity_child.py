from datetime import datetime
from typing import Optional, List

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.achievments_child import AchievementsChild
from portfolio.models.events_child import EventsChild


class ActivityChild(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 list_events_child: Optional[List[EventsChild]] = None,
                 list_achievements_child: Optional[List[AchievementsChild]] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__list_events_child = list_events_child
        self.__list_achievements_child = list_achievements_child

    @property
    def list_events_child(self):
        return self.__list_events_child

    @list_events_child.setter
    def list_events_child(self, value: List[EventsChild]):
        self.__list_events_child = value

    @property
    def list_achievements_child(self):
        return self.__list_achievements_child

    @list_achievements_child.setter
    def list_achievements_child(self, value: List[AchievementsChild]):
        self.__list_achievements_child = value
