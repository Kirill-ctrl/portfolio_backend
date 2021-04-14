from portfolio.internal.biz.serializers.parents import ParentsSerializer, SER_FOR_ADD_PARENTS
from portfolio.models.parents import Parents


def get_response_add_parents(parents: Parents):
    return ParentsSerializer.serialize(parents, SER_FOR_ADD_PARENTS)


def get_response_edit_parents(parents: Parents):
    return ParentsSerializer.serialize(parents, SER_FOR_EDIT_PARENTS)