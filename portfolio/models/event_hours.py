from datetime import datetime, date
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.events import Events


class EventHours(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 events: Optional[Events] = None,
                 hours: Optional[int] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__events = events
        self.__hours = hours

    @property
    def events(self) -> Events:
        return self.__events

    @property
    def hours(self) -> int:
        return self.__hours
