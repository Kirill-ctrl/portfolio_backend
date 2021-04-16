from flask import request, json

from portfolio.internal.biz.services.teacher import TeacherService
from portfolio.internal.middlewares.organisation import get_org_id_and_acc_id_with_confirmed_email
from portfolio.models.account_main import AccountMain
from portfolio.models.organisation import Organisation
from portfolio.models.teacher import Teacher


def get_teacher_id_and_org_id(func):
    @get_org_id_and_acc_id_with_confirmed_email
    def wrapper(*args, auth_account_main_id: int, organisation_id: int, **kwargs):
        if not request.args.get('teacher'):
            return json.dumps("Прикрепите учителя")
        teacher = Teacher(
            name=request.args.get('teacher').split(' ')[0],
            surname=request.args.get('teacher').split(' ')[1],
            organisation=Organisation(id=organisation_id,
                                      account_main=AccountMain(id=auth_account_main_id))
        )

        teacher, err = TeacherService.get_by_organisation_id(teacher)
        if err:
            return json.dumps(err)

        response = func(*args, organisation_id=teacher.organisation.id, teacher_id=teacher.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper
