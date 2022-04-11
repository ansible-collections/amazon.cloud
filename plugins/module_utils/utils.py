import re
import json
import functools
from typing import Iterable, List, Dict

from ansible.module_utils.common.dict_transformations import (
    camel_dict_to_snake_dict,
    snake_dict_to_camel_dict,
)

from ansible.module_utils._text import to_native


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
    if properties and "Tags" in properties:
        properties["tags"] = boto3_tag_list_to_ansible_dict(properties["Tags"])
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


def scrub_keys(a_dict: Dict, list_of_keys_to_remove: List[str]) -> Dict:
    """Filter a_dict by removing unwanted key: values listed in list_of_keys_to_remove"""
    if not isinstance(a_dict, dict):
        return a_dict
    return {k: v for k, v in a_dict.items() if k not in list_of_keys_to_remove}


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
