from datetime import datetime
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.account_main import AccountMain


class Parents(AbstractModel):
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 account_main: Optional[AccountMain] = None,
                 name: Optional[str] = None,
                 surname: Optional[str] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__account_main = account_main
        self.__name = name
        self.__surname = surname

    @property
    def account_main(self) -> AccountMain:
        return self.__account_main

    @property
    def name(self) -> str:
        return self.__name

    @property
    def surname(self) -> str:
        return self.__surname
