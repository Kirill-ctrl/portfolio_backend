from portfolio.internal.biz.dao.parents import ParentsDao
from portfolio.models.parents import Parents


class ParentsService:

    @staticmethod
    def add_parent(parents: Parents):
        parents, err = ParentsDao().add(parents)
        if err:
            return None, err

        return parents, None

    @staticmethod
    def update_parent(parents: Parents):
        parents, err = ParentsDao().update(parents.account_main.id, parents)
        if err:
            return None, err
        return parents, None
