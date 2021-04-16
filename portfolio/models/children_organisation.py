from datetime import datetime, date
from typing import Optional

from portfolio.models.abstract_model import AbstractModel
from portfolio.models.children import Children
from portfolio.models.teacher import Teacher


class ChildrenOrganisation(AbstractModel):

    def __init__(self,
                 id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 edited_at: Optional[datetime] = None,
                 teacher: Optional[Teacher] = None,
                 children: Optional[Children] = None):
        super().__init__(id=id, created_at=created_at, edited_at=edited_at)
        self.__teacher = teacher
        self.__children = children

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, value: Teacher):
        self.__teacher = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value: Children):
        self.__children = value
