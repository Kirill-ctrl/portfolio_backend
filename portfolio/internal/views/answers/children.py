from portfolio.internal.biz.serializers.children import ChildrenSerializer, SER_FOR_ADD_CHILD
from portfolio.models.children import Children


def get_response_add_children(children: Children):
    return ChildrenSerializer.serialize(children, SER_FOR_ADD_CHILD)