from datetime import datetime, date
from typing import Optional

from portfolio.models.abstract_model import AbstractModel


class Events(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 type: Optional[str] = None,
                 name: Optional[str] = None,
                 date_event: Optional[date] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__type = type
        self.__name = name
        self.__date_event = date_event

    @property
    def type(self) -> str:
        return self.__type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def date_event(self) -> date:
        return self.__date_event
