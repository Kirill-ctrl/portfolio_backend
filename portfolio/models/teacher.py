from datetime import datetime
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.organisation import Organisation


class Teacher(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 organisation: Optional[Organisation] = None,
                 name: Optional[str] = None,
                 surname: Optional[str] = None,
                 specialty: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__organisation = organisation
        self.__name = name
        self.__surname = surname
        self.__specialty = specialty

    @property
    def organisation(self) -> Organisation:
        return self.__organisation

    @organisation.setter
    def organisation(self, value: Organisation):
        self.__organisation = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def surname(self) -> str:
        return self.__surname

    @property
    def specialty(self) -> str:
        return self.__specialty
