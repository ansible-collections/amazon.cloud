import json
from typing import Iterable, List

from ansible.module_utils.common.dict_transformations import (
    camel_dict_to_snake_dict,
    snake_dict_to_camel_dict,
)


def _jsonify(data):
    identifier = data.get("Identifier", None)
    properties = data.get("Properties", None)
    # Convert the Resource Properties from a str back to json
    data = {"identifier": identifier, "properties": json.loads(properties)}
    return data


def normalize_response(response: Iterable):
    result: List = []

    resource_descriptions = response.get("ResourceDescription", {}) or response.get(
        "ResourceDescriptions", []
    )
    if isinstance(resource_descriptions, list):
        res = [_jsonify(r_d) for r_d in resource_descriptions]
        _result = [camel_dict_to_snake_dict(r) for r in res]
        result.append(_result)
    else:
        result.append(_jsonify(resource_descriptions))
        result = [camel_dict_to_snake_dict(res) for res in result]

    return result


class JsonPatch(list):
    def __str__(self):
        return json.dumps(self)


def list_merge(old, new):
    l = []
    for i in old + new:
        if i not in l:
            l.append(i)
    return l


def op(operation, path, value):
    path = "/{0}".format(path.lstrip("/"))
    return {"op": operation, "path": path, "value": value}


# This is a rather naive implementation. Dictionaries within
# lists and lists within dictionaries will not be merged.
def make_op(path, old, new, strategy):
    if isinstance(old, dict):
        if strategy == "merge":
            new = dict(old, **new)
    elif isinstance(old, list):
        if strategy == "merge":
            new = list_merge(old, new)
    return op("replace", path, new)
