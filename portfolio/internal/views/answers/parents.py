from portfolio.internal.biz.serializers.parents import ParentsSerializer, SER_FOR_ADD_PARENTS, SER_FOR_EDIT_PARENTS, \
    SER_FOR_DELETE_PARENTS
from portfolio.models.parents import Parents


def get_response_add_parents(parents: Parents):
    return ParentsSerializer.serialize(parents, SER_FOR_ADD_PARENTS)


def get_response_edit_parent(parents: Parents):
    return ParentsSerializer.serialize(parents, SER_FOR_EDIT_PARENTS)


def get_response_delete_parent(parents: Parents):
    return ParentsSerializer.serialize(parents, SER_FOR_DELETE_PARENTS)