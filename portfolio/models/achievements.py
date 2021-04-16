from datetime import datetime
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.events import Events


class Achievements(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 events: Optional[Events] = None,
                 name: Optional[str] = None,
                 point: Optional[int] = None,
                 nomination: Optional[str] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__events = events
        self.__name = name
        self.__point = point
        self.__nomination = nomination

    @property
    def events(self) -> Events:
        return self.__events

    @property
    def point(self) -> int:
        return self.__point

    @property
    def nomination(self) -> str:
        return self.__nomination

    @property
    def name(self) -> str:
        return self.__name
