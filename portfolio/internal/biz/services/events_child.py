from portfolio.internal.biz.dao.achievements_child import AchievementsChildDao
from portfolio.internal.biz.dao.events_child import EventsChildDao
from portfolio.models.activity_child import ActivityChild
from portfolio.models.events_child import EventsChild


class EventsChildService:

    @staticmethod
    def update_status(events_child: EventsChild):
        events_child, err = EventsChildDao().update_status(events_child)
        if err:
            return None, err

        return events_child, None

    @staticmethod
    def get_by_children_org_id(children_organisation_id: int):
        list_events_child, err = EventsChildDao().get_by_child_organisation_id_or_child_id(children_organisation_id=children_organisation_id)
        if err:
            return None, err

        list_achievements_child, err = AchievementsChildDao().get_by_children_organisation_id_or_child_id(children_organisation_id=children_organisation_id)
        if err:
            return None, err

        list_activity_child = ActivityChild(
            list_events_child=list_events_child,
            list_achievements_child=list_achievements_child
        )
        return list_activity_child, None

    @staticmethod
    def get_by_children_id(events_child: EventsChild):
        list_events_child, err = EventsChildDao().get_by_child_organisation_id_or_child_id(children_id=events_child.children_organisation.children.id)
        if err:
            return None, err

        list_achievements_child, err = AchievementsChildDao().get_by_children_organisation_id_or_child_id(children_id=events_child.children_organisation.children.id)
        if err:
            return None, err

        list_activity_child = ActivityChild(
            list_events_child=list_events_child,
            list_achievements_child=list_achievements_child
        )
        return list_activity_child, None
