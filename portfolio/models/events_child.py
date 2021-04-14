from datetime import datetime
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.children import Children
from portfolio.models.events import Events


class EventsChild(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 events: Optional[Events] = None,
                 children: Optional[Children] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__events = events
        self.__children = children

    @property
    def events(self) -> Events:
        return self.__events

    @property
    def children(self) -> Children:
        return self.__children
