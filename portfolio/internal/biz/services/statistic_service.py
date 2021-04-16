from datetime import datetime

from portfolio.internal.biz.dao.children_organisation import ChildrenOrganisationDao
from portfolio.internal.biz.dao.events import EventsDao


class StatisticService:

    @staticmethod
    def get_result_statistic(result_sort_statistic: datetime.date,
                             children_id: int):
        organisation_hours_with_period_dict, err = ChildrenOrganisationDao().get_statistic_by_sort_date(result_sort_statistic, children_id)
        if err:
            return None, err
        return organisation_hours_with_period_dict, None

    @staticmethod
    def get_result_focus(result_sort_focus: datetime.date,
                         children_id: int):
        event_focus_dict, err = EventsDao().get_focus_by_sort_date(result_sort_focus,
                                                                   children_id)
        if err:
            return event_focus_dict, None
        return event_focus_dict, None
