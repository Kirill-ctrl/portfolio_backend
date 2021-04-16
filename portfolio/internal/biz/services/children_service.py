from portfolio.internal.biz.dao.children import ChildrenDao
from portfolio.models.children import Children


class ChildrenService:

    @staticmethod
    def add_child(children: Children):
        children, err = ChildrenDao().add(children)
        if err:
            return None, err
        return children, None

    @staticmethod
    def get_child(children: Children):
        children, err = ChildrenDao().get_by_parents_id(children)
        if err:
            return None, err
        return children, None

    @staticmethod
    def get_children_by_parents_id(children: Children):
        list_children, err = ChildrenDao().get_all_by_parents_id(children)
        if err:
            return None, err
        return list_children, None
