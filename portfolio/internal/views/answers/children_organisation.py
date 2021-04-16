from typing import List

from portfolio.internal.biz.serializers.activity_child import ActivityChildSerializer, SER_FOR_GET_ALL_DETAIL_LEARNER
from portfolio.internal.biz.serializers.children_organisation import ChildrenOrganisationSerializer, \
    SER_FOR_GET_LIST_LEARNERS
from portfolio.models.activity_child import ActivityChild
from portfolio.models.children_organisation import ChildrenOrganisation


def get_response_list_children_organisation(list_learners: List[ChildrenOrganisation]):
    return ChildrenOrganisationSerializer.serialize(list_learners, SER_FOR_GET_LIST_LEARNERS)


def get_response_detail_activity_child_organisation(list_activity_child: ActivityChild):
    return ActivityChildSerializer.serialize(list_activity_child, SER_FOR_GET_ALL_DETAIL_LEARNER)
