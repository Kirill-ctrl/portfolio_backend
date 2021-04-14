from portfolio.internal.biz.dao.children import ChildrenDao
from portfolio.models.children import Children


class ChildrenService:

    @staticmethod
    def add_child(children: Children):
        children, err = ChildrenDao().add(children)
        if err:
            return None, err
        return children, None
