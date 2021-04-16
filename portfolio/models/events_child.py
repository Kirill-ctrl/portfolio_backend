from datetime import datetime
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events import Events


class EventsChild(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 events: Optional[Events] = None,
                 children_organisation: Optional[ChildrenOrganisation] = None,
                 status: Optional[bool] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__events = events
        self.__children_organisation = children_organisation
        self.__status = status

    @property
    def events(self) -> Events:
        return self.__events

    @events.setter
    def events(self, value: Events):
        self.__events = value

    @property
    def children_organisation(self) -> ChildrenOrganisation:
        return self.__children_organisation

    @children_organisation.setter
    def children_organisation(self, value: ChildrenOrganisation):
        self.__children_organisation = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: bool):
        self.__status = value
