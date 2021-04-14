from datetime import datetime
from typing import Optional


class AbstractModel:
    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None) -> None:
        self.__id = id
        self.__created_at = created_at
        self.__edited_at = edited_at

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    @property
    def edited_at(self) -> datetime:
        return self.__edited_at

    @edited_at.setter
    def edited_at(self, value):
        self.__edited_at = value
