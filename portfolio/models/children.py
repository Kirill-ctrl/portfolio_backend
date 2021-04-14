from datetime import datetime, date
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_main import AccountMain
from portfolio.models.parents import Parents


class Children(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 account_main: Optional[AccountMain] = None,
                 parents: Optional[Parents] = None,
                 name: Optional[str] = None,
                 surname: Optional[str] = None,
                 date_born: Optional[date] = None) -> None:
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__account_main = account_main
        self.__parents = parents
        self.__name = name
        self.__surname = surname
        self.__date_born = date_born

    @property
    def account_main(self) -> AccountMain:
        return self.__account_main

    @property
    def parents(self) -> Parents:
        return self.__parents

    @property
    def name(self) -> str:
        return self.__name

    @property
    def surname(self) -> str:
        return self.__surname

    @property
    def date_born(self) -> date:
        return self.__date_born