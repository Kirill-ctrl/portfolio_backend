import copy
from typing import Mapping


def filter_keys_by_substr(obj: Mapping, substr: str) -> dict:
    new_dict = copy.deepcopy(dict(obj))

    for key in list(new_dict.keys()):
        i = key.find(substr)
        if i != -1:
            new_key = key[i:]
            if new_key != key:
                new_dict[new_key] = new_dict[key]
                del new_dict[key]
        else:
            del new_dict[key]

    return new_dict
