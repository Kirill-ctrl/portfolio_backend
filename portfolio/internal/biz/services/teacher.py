from portfolio.internal.biz.dao.teacher import TeacherDao
from portfolio.models.teacher import Teacher


class TeacherService:

    @staticmethod
    def add_teacher(teacher: Teacher):
        teacher, err = TeacherDao().add(teacher)
        if err:
            return None, err

        return teacher, None

    @staticmethod
    def edit_teacher(teacher: Teacher):
        teacher, err = TeacherDao().update(teacher.organisation.id, teacher)
        if err:
            return None, err

        return teacher, None

    @staticmethod
    def delete_teacher(teacher: Teacher):
        teacher, err = TeacherDao().remove(teacher)
        if err:
            return None, err
        return teacher, None

    @staticmethod
    def get_by_organisation_id(teacher: Teacher):
        teacher, err = TeacherDao().get_id_by_organisation_id(teacher)
        if err:
            return None, err
        return teacher, None
