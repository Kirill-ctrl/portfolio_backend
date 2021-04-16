from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.organisation import Organisation

DES_FROM_ADD_ORGANISATION = 'des-from-add-organisation'
DES_FOR_EDIT_ORGANISATION = 'des-from-edit-organisation'
DES_FROM_DB_DETAIL_ORGANISATION = 'des-from-db-detail-organisation'
DES_FROM_DB_FULL_ORGANISATION = 'des-from-db-full-organisation'
DES_FROM_DB_GET_ORGANISATION = 'des_from_db_get_organisation'


class OrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_ADD_ORGANISATION:
            return cls._des_organisation_add
        elif format_des == DES_FOR_EDIT_ORGANISATION:
            return cls._des_organisation_edit
        elif format_des == DES_FROM_DB_DETAIL_ORGANISATION:
            return cls._des_from_db_detail_organisation
        elif format_des == DES_FROM_DB_DETAIL_ORGANISATION:
            return cls._des_from_db_full_organisation
        elif format_des == DES_FROM_DB_GET_ORGANISATION:
            return cls._des_from_db_get_organisation
        else:
            raise TypeError

    @staticmethod
    def _des_organisation_add(organisation_dict):
        return Organisation(
            name=organisation_dict.get('name'),
            login=organisation_dict.get('login'),
            photo_link=organisation_dict.get('photo_link'),
            description=organisation_dict.get('description')
        )

    @staticmethod
    def _des_organisation_edit(organisation_dict):
        return Organisation(
            name=organisation_dict.get('name') if organisation_dict.get('name') else '-1',
            login=organisation_dict.get('login') if organisation_dict.get('login') else '-1',
            photo_link=organisation_dict.get('photo_link') if organisation_dict.get('photo_link') else '-1',
            description=organisation_dict.get('description') if organisation_dict.get('description') else '-1'
        )

    @staticmethod
    def _des_from_db_detail_organisation(data):
        return Organisation(
            id=data['organisation_id'],
            created_at=data['organisation_created_at'],
            name=data['organisation_name'],
            photo_link=data['organisation_photo_link'],
            description=data['organisation_description']
        )

    @staticmethod
    def _des_from_db_full_organisation(data):
        return [
            Organisation(
                id=data[i]['organisation_id'],
                name=data[i]['organisation_name'],
                login=data[i]['organisation_login'],
                photo_link=data[i]['organisation_photo_link'],
                description=data[i]['organisation_description']
            )
            for i in range(len(data))
        ]

    @staticmethod
    def _des_from_db_get_organisation(data):
        return Organisation(
            id=data['organisation_id'],
            name=data['organisation_name'],
            login=data['organisation_login'],
            photo_link=data['organisation_photo_link'],
            description=data['organisation_description'],
        )