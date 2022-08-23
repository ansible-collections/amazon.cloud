import re
import copy
import json
import functools
import traceback
from typing import Iterable, List, Dict, Union

JSON_PATCH_IMPORT_ERR = None
try:
    import jsonpatch

    HAS_JSON_PATCH = True
except ImportError:
    HAS_JSON_PATCH = False
    JSON_PATCH_IMPORT_ERR = traceback.format_exc()

from ansible.module_utils.common.dict_transformations import (
    camel_dict_to_snake_dict,
    snake_dict_to_camel_dict,
    recursive_diff,
)

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import missing_required_lib


def to_async(fn):
    """Turn a sync function into an async function using threads"""
    from concurrent.futures import ThreadPoolExecutor
    import asyncio

    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def to_sync(fn):
    """Turn an async function into a sync function"""
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def _jsonify(data: Dict) -> Dict:
    identifier = data.get("Identifier", None)
    # Convert the Resource Properties from a str back to json
    properties = json.loads(data.get("Properties", None))
    data = {"identifier": identifier, "properties": properties}
    return data


def camel_to_snake(name: str, reversible: bool = False) -> str:
    def prepend_underscore_and_lower(m):
        return "_" + m.group(0).lower()

    if reversible:
        upper_pattern = r"[A-Z]"
    else:
        # Cope with pluralized abbreviations such as TargetGroupARNs
        # that would otherwise be rendered target_group_ar_ns
        upper_pattern = r"[A-Z]{3,}s$"

    s1 = re.sub(upper_pattern, prepend_underscore_and_lower, name)
    # Handle when there was nothing before the plural_pattern
    if s1.startswith("_") and not name.startswith("_"):
        s1 = s1[1:]
    if reversible:
        return s1

    # Remainder of solution seems to be https://stackoverflow.com/a/1176023
    first_cap_pattern = r"(.)([A-Z][a-z]+)"
    all_cap_pattern = r"([a-z0-9])([A-Z]+)"
    s2 = re.sub(first_cap_pattern, r"\1_\2", s1)
    return re.sub(all_cap_pattern, r"\1_\2", s2).lower()


def snake_to_camel(snake, capitalize_first=False):
    if capitalize_first:
        return "".join(x.capitalize() or "_" for x in snake.split("_"))
    else:
        return snake.split("_")[0] + "".join(
            x.capitalize() or "_" for x in snake.split("_")[1:]
        )


def scrub_keys(a_dict: Dict, list_of_keys_to_remove: List[str]) -> Dict:
    """Filter a_dict by removing unwanted key: values listed in list_of_keys_to_remove"""
    if not isinstance(a_dict, dict):
        return a_dict
    return {k: v for k, v in a_dict.items() if k not in list_of_keys_to_remove}


def normalize_response(response: Iterable):
    resource_descriptions = response.get("ResourceDescription", {}) or response.get(
        "ResourceDescriptions", []
    )

    def _normalize_response(resource_description):
        json_res = _jsonify(resource_description)
        snaked_res = camel_dict_to_snake_dict(json_res)
        if "tags" in snaked_res["properties"]:
            snaked_res["properties"]["tags"] = boto3_tag_list_to_ansible_dict(
                snaked_res["properties"]["tags"]
            )
        return snaked_res

    if isinstance(resource_descriptions, list):
        return [_normalize_response(resource) for resource in resource_descriptions]
    else:
        return _normalize_response(resource_descriptions)


def ansible_dict_to_boto3_tag_list(
    tags_dict, tag_name_key_name="Key", tag_value_key_name="Value"
):
    """
    Convert a flat dict of key:value pairs representing AWS resource tags to a boto3 list of dicts
    Args:
        tags_dict (dict): Dict representing AWS resource tags.
        tag_name_key_name (str): Value to use as the key for all tag keys (useful because boto3 doesn't always use "Key")
        tag_value_key_name (str): Value to use as the key for all tag values (useful because boto3 doesn't always use "Value")
    Basic Usage:
        >>> tags_dict = {'MyTagKey': 'MyTagValue'}
        >>> ansible_dict_to_boto3_tag_list(tags_dict)
        {
            'MyTagKey': 'MyTagValue'
        }
    Returns:
        List: List of dicts containing tag keys and values
        [
            {
                'Key': 'MyTagKey',
                'Value': 'MyTagValue'
            }
        ]
    """

    if not tags_dict:
        return []

    tags_list = []
    for k, v in tags_dict.items():
        tags_list.append({tag_name_key_name: k, tag_value_key_name: to_native(v)})

    return tags_list


def boto3_tag_list_to_ansible_dict(
    tags_list, tag_name_key_name=None, tag_value_key_name=None
):

    """Convert a boto3 list of resource tags to a flat dict of key:value pairs
    Args:
        tags_list (list): List of dicts representing AWS tags.
        tag_name_key_name (str): Value to use as the key for all tag keys (useful because boto3 doesn't always use "Key")
        tag_value_key_name (str): Value to use as the key for all tag values (useful because boto3 doesn't always use "Value")
    Basic Usage:
        >>> tags_list = [{'Key': 'MyTagKey', 'Value': 'MyTagValue'}]
        >>> boto3_tag_list_to_ansible_dict(tags_list)
        [
            {
                'Key': 'MyTagKey',
                'Value': 'MyTagValue'
            }
        ]
    Returns:
        Dict: Dict of key:value pairs representing AWS tags
         {
            'MyTagKey': 'MyTagValue',
        }
    """

    if tag_name_key_name and tag_value_key_name:
        tag_candidates = {tag_name_key_name: tag_value_key_name}
    else:
        tag_candidates = {"key": "value", "Key": "Value"}

    # minio seems to return [{}] as an empty tags_list
    if not tags_list or not any(tag for tag in tags_list):
        return {}
    for k, v in tag_candidates.items():
        if k in tags_list[0] and v in tags_list[0]:
            return dict((tag[k], tag[v]) for tag in tags_list)
    raise ValueError(
        "Couldn't find tag key (candidates %s) in tag list %s"
        % (str(tag_candidates), str(tags_list))
    )


def diff_dicts(existing: Dict, new: Dict) -> Union[bool, Dict]:
    result: Dict = {}

    diff = recursive_diff(existing, new)

    if not diff:
        return True, {}

    result["before"] = diff[0]
    result["after"] = diff[1]

    return False, result


def json_patch(existing, patch):
    if not HAS_JSON_PATCH:
        error = {
            "msg": missing_required_lib("jsonpatch"),
            "exception": JSON_PATCH_IMPORT_ERR,
        }
        return None, error
    try:
        patch = jsonpatch.JsonPatch(patch)
        patched = patch.apply(existing)
        return patched, None
    except jsonpatch.InvalidJsonPatch as e:
        error = {"msg": "Invalid JSON patch", "exception": e}
        return None, error
    except jsonpatch.JsonPatchConflict as e:
        error = {"msg": "Patch could not be applied due to a conflict", "exception": e}
        return None, error


class JsonPatch(list):
    def __str__(self):
        return json.dumps(self)


def find_tag_by_key(key, tags):
    for tag in tags:
        if tag["Key"] == key:
            return tag


def tag_merge(t1, t2):
    for tag in t2:
        existing = find_tag_by_key(tag["Key"], t1)
        if existing:
            existing["Value"] = tag["Value"]
        else:
            t1.append(tag)
    return t1


def op(operation, path, value):
    path = "/{0}".format(path.lstrip("/"))
    return {"op": operation, "path": path, "value": value}


def make_op(path, old, new, strategy):
    _new_cpy = copy.deepcopy(new)

    if isinstance(old, dict):
        if strategy == "merge":
            _new_cpy = dict(old, **new)
    elif isinstance(old, list):
        if strategy == "merge":
            _old_cpy = copy.deepcopy(old)
            _new_cpy = tag_merge(_old_cpy, new)

    return op("replace", path, _new_cpy)


def get_patch(module, params, properties):
    patch = JsonPatch()

    for k, v_in in params.items():
        strategy = "merge"
        if k in properties:
            v_exisiting = properties.get(k)
            # Continue loop if both values are equal
            if v_in == v_exisiting:
                continue
            # Compare lists contents, not order (i.e. list of tag dicts)
            if isinstance(v_in, list) and isinstance(v_exisiting, list):
                if [tag for tag in v_in if tag not in v_exisiting] == [] and [
                    tag for tag in v_exisiting if tag not in v_in
                ] == []:
                    continue
            # If purge, then replace old resource
            if module.params.get("purge_{0}".format(k.lower())):
                strategy = "replace"
            # Add difference to JSON patch
            patch.append(make_op(k, v_exisiting, v_in, strategy))
        else:
            # Add patch if key isnt in properties - dont add tags if tags = {} and no tags on resource
            if k == "Tags" and v_in == [] and "tags" not in properties:
                continue
            patch.append(op("add", k, v_in))

    return patch
