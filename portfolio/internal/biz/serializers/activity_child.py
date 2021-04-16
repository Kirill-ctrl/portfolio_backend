from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
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
            'children': {
                'id': activity_child.list_events_child[0].children_organisation.children.id,
                'name': activity_child.list_events_child[0].children_organisation.children.name,
                'surname': activity_child.list_events_child[0].children_organisation.children.surname,
                'date_born': activity_child.list_events_child[0].children_organisation.children.date_born,
                'parents': {
                    'id': activity_child.list_events_child[0].children_organisation.children.parents.id
                }
            },
            'events_child': [
                {
                    'id': activity_child.list_events_child[i].id,
                    'status': activity_child.list_events_child[i].status,
                    'event': {
                        'id': activity_child.list_events_child[i].events.id,
                        'type': activity_child.list_events_child[i].events.type,
                        'name': activity_child.list_events_child[i].events.name,
                        'date_event': activity_child.list_events_child[i].events.date_event,
                        'hours': activity_child.list_events_child[i].events.hours,
                        'skill': activity_child.list_events_child[i].events.skill
                    },
                    'children_organisation': {
                        activity_child.list_events_child[i].children_organisation.id
                    }
                }
                for i in range(len(activity_child.list_events_child))
            ],
            'achievements': [
                {
                    'id': activity_child.list_achievements_child[i].achievements.id,
                    'achievement': {
                        'id': activity_child.list_achievements_child[i].achievements.id,
                        'event': {
                            'id': activity_child.list_achievements_child[i].achievements.events.id
                        },
                        'name': activity_child.list_achievements_child[i].achievements.name,
                        'point': activity_child.list_achievements_child[i].achievements.point,
                        'nomination': activity_child.list_achievements_child[i].achievements.nomination
                    }
                }
                for i in range(len(activity_child.list_achievements_child))
            ],
            'count_hours': get_count_hours_in_events(activity_child.list_events_child),
            'count_events': len(activity_child.list_events_child),
            'count_achievements': len(activity_child.list_achievements_child)
        }
