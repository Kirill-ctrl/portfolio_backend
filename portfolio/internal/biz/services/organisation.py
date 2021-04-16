from portfolio.internal.biz.dao.organisation import OrganisationDao
from portfolio.models.organisation import Organisation


class OrganisationService:

    @staticmethod
    def add_organisation(organisation: Organisation):
        organisation, err = OrganisationDao().add(organisation)
        if err:
            return None, err
        return organisation, None

    @staticmethod
    def edit_organisation(organisation: Organisation):
        organisation, err = OrganisationDao().update(organisation.account_main.id, organisation)
        if err:
            return None, err
        return organisation, None

    @staticmethod
    def delete_organisation(organisation: Organisation):
        organisation, err = OrganisationDao().remove(organisation)
        if err:
            return None, err
        return organisation, None

    @staticmethod
    def get_by_account_id(account_main_id):
        organisation, err = OrganisationDao().get_by_id(account_main_id)
        if err:
            return None, err
        return organisation, None

    @staticmethod
    def get_all_by_account_id(account_main_id):
        list_teacher_organisation, err = OrganisationDao().get_all_by_account_id(account_main_id)
        if err:
            return None, err
        return list_teacher_organisation, None

    @staticmethod
    def get_all_organisations():
        list_organisations, err = OrganisationDao().get_all()
        if err:
            return None, err
        return list_organisations, None

    @staticmethod
    def get_by_organisation_id(organisation_id: int):
        organisation, err = OrganisationDao().get_by_org_id(organisation_id)
        if err:
            return None, err
        return organisation, None
