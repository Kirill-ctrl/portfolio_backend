from portfolio.internal.biz.serializers.achievements import AchievementsSerializer, SER_FOR_DETAIL_ACHIEVEMENTS_CHILD
from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.children import ChildrenSerializer, SER_FOR_GET_DETAIL_CHILDREN
from portfolio.internal.biz.serializers.children_organisation import ChildrenOrganisationSerializer
from portfolio.internal.biz.serializers.events_child import EventsChildSerializer, SER_FOR_DETAIL_EVENTS_CHILD
from portfolio.internal.biz.serializers.utils import get_count_hours_in_events
from portfolio.models.activity_child import ActivityChild

SER_FOR_GET_ALL_DETAIL_LEARNER = 'ser-for-get-all-detail-learner'


class ActivityChildSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_GET_ALL_DETAIL_LEARNER:
            return cls._ser_for_get_all_detail_learner
        else:
            raise TypeError

    @staticmethod
    def _ser_for_get_all_detail_learner(activity_child: ActivityChild):
        return {
            'children': ChildrenSerializer.serialize(activity_child.list_events_child[0].children_organisation.children,
                                                     SER_FOR_GET_DETAIL_CHILDREN),
            'events_child': [
                EventsChildSerializer.serialize(activity_child.list_events_child[i], SER_FOR_DETAIL_EVENTS_CHILD)
                for i in range(len(activity_child.list_events_child))
            ],
            'achievements': [
                AchievementsSerializer.serialize(activity_child.list_achievements_child[i].achievements,
                                                 SER_FOR_DETAIL_ACHIEVEMENTS_CHILD)
                for i in range(len(activity_child.list_achievements_child))
            ] if activity_child.list_achievements_child else None,
            'count_hours': get_count_hours_in_events(activity_child.list_events_child),
            'count_events': len(activity_child.list_events_child),
            'count_achievements': len(activity_child.list_achievements_child) if activity_child.list_achievements_child else None
        }
