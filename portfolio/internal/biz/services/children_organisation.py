from portfolio.internal.biz.dao.children_organisation import ChildrenOrganisationDao


class ChildrenOrganisationService:

    @staticmethod
    def get_all_by_org_id(organisation_id: int):
        list_learners, err = ChildrenOrganisationDao().get_all_by_organisation_id(organisation_id)
        if err:
            return None, err
        return list_learners, None
