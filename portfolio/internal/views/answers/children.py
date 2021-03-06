from typing import List

from portfolio.internal.biz.serializers.activity_child import ActivityChildSerializer, SER_FOR_GET_ALL_DETAIL_LEARNER
from portfolio.internal.biz.serializers.children import ChildrenSerializer, SER_FOR_ADD_CHILD, SER_FOR_GET_LIST_CHILDREN
from portfolio.models.activity_child import ActivityChild
from portfolio.models.children import Children


def get_response_add_children(children: Children):
    return ChildrenSerializer.serialize(children, SER_FOR_ADD_CHILD)


def get_response_detail_activity_children(list_activity_child: ActivityChild):
    return ActivityChildSerializer.serialize(list_activity_child, SER_FOR_GET_ALL_DETAIL_LEARNER)


def get_response_get_list_child(list_children: List[Children]):
    return ChildrenSerializer.serialize(list_children, SER_FOR_GET_LIST_CHILDREN)
