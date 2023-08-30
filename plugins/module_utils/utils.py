# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import re
import copy
import json
import functools
import traceback
from collections import OrderedDict
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
    recursive_diff,
)

# pylint: disable=unused-import
from ansible.module_utils.common.dict_transformations import (
    snake_dict_to_camel_dict,
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


def map_key_to_alias(data: Dict, mapping: Dict) -> Dict:
    # Ensures the alias is passed to the API call
    mapped_data: Dict = {}

    for key, value in data.items():
        if key in mapping:
            mapped_key = mapping[key].get("aliases", [key])[0]
            if isinstance(value, dict):
                mapped_data[mapped_key] = map_key_to_alias(
                    value,
                    mapping[key].get("options", {})
                    or mapping[key].get("suboptions", {}),
                )
            elif isinstance(value, list):
                mapped_data[mapped_key] = []
                for item in value:
                    if isinstance(item, dict):
                        mapped_data[mapped_key].append(
                            map_key_to_alias(
                                item,
                                mapping[key].get("options", {})
                                or mapping[key].get("suboptions", {}),
                            )
                        )
                    else:
                        mapped_data[mapped_key] = value
            else:
                mapped_data[mapped_key] = value
        else:
            mapped_data[key] = value
    return mapped_data


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


def safe_json(data):
    try:
        json_object = json.loads(data)
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        if "Expecting property name enclosed in double quotes" in str(e):
            json_string_fixed = data.replace("'", '"')
            json_object = safe_json(json_string_fixed)
        else:
            # Return data as is
            return data
    return json_object


def helper_sort_dict(obj):
    """
    Order a nested complex dictionary
    """
    if isinstance(obj, dict):
        obj = OrderedDict(sorted(obj.items()))
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                obj[k] = helper_sort_dict(v)

    if isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict) or isinstance(v, list):
                obj[i] = helper_sort_dict(v)
        obj = sorted(obj, key=lambda x: json.dumps(x))

    return obj


def merge_lists(list1, list2):
    merged_list: List = []
    matched_list: List = []

    for dict1 in list1:
        if isinstance(dict1, dict):
            dict1 = helper_sort_dict(dict1)
            merged_dict = dict1.copy()
        else:
            merged_dict = dict1

        for dict2 in list2:
            if isinstance(dict1, dict) and isinstance(dict2, dict):
                dict2 = helper_sort_dict(dict2)
                for key in dict2:
                    if dict1.get(key) == dict2.get(key):
                        # Enforce matching between dictionaries
                        if all(type(dict1[key]) == type(dict2[key]) for key in dict1):
                            if dict1 == dict2:
                                # They match, nothing further to do, just append dict1 to merged_list
                                if dict1 not in merged_list:
                                    merged_list.append(dict1)
                                    matched_list.append(dict1)
                            else:
                                # They have the same value types, but do not match
                                merged_dict = recursive_merge(merged_dict, dict2)
                                matched_list.append(dict1)
                                matched_list.append(dict2)
                                if merged_dict not in merged_list:
                                    merged_list.append(merged_dict)
                                    matched_list.append(merged_dict)
                    else:
                        # They do not have anything in common, just add both to merge_list and matched_list
                        if dict1 not in merged_list and dict1 not in matched_list:
                            merged_list.append(dict1)
                            matched_list.append(dict1)
                        if dict2 not in merged_list and dict2 not in matched_list:
                            # Add dict2 if already not present in merged_list
                            merged_list.append(dict2)
                            matched_list.append(dict2)
            else:
                if dict2 not in merged_list:
                    merged_list.append(dict2)

    return merged_list


def merge_list_of_dicts(list1: List, list2) -> List:
    # Handle when list of dicts (different than Tags and different key names) need to be merged
    merged_list = list1.copy()

    for dict2 in list2:
        matching_indices = [
            i for i, item1 in enumerate(merged_list) if any(k in item1 for k in dict2)
        ]

        if matching_indices:
            for index in matching_indices:
                if isinstance(merged_list, list):
                    dict1 = merged_list[index]
                    if isinstance(dict2, dict) and isinstance(dict1, dict):
                        for key, value in dict2.items():
                            value_dict = safe_json(value)
                            if (
                                dict1.get(key, {})
                                and isinstance(value_dict, dict)
                                and isinstance(dict1[key], dict)
                            ):
                                dict1[key] = recursive_merge(dict1[key], value_dict)
                            elif (
                                dict1.get(key, [])
                                and isinstance(value_dict, list)
                                and isinstance(dict1[key], list)
                            ):
                                # Easy merge
                                if all(
                                    isinstance(item, (str, int, float))
                                    for item in dict1[key]
                                ):
                                    dict1[key] = sorted(
                                        list(set(dict1[key]).union(value_dict))
                                    )
                                else:
                                    dict1[key] = merge_lists(dict1[key], value_dict)
                            else:
                                dict1[key] = value_dict
        else:
            # else: there's no matching, so just add dict2 to merged_list
            merged_list.append(dict2)

    return merged_list


def recursive_merge(dict1: Dict, dict2: Dict) -> Dict:
    merged = dict1.copy()

    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = recursive_merge(merged[key], value)
        if key in merged and isinstance(merged[key], list) and isinstance(value, list):
            # Easy merge
            if all(isinstance(item, (str, int, float)) for item in merged[key]):
                dict1[key] = sorted(list(set(merged[key]).union(value)))
            else:
                merged[key] = merge_lists(merged[key], value)
        else:
            merged[key] = value

    return merged


class QuoteSwappingEncoder(json.JSONEncoder):
    def encode(self, obj):
        def swap_quotes(item):
            if isinstance(item, str):
                return (
                    item.replace("'", "__TEMP_SINGLE_QUOTE__")
                    .replace('"', "'")
                    .replace("__TEMP_SINGLE_QUOTE__", '"')
                )
            return item

        return super().encode(swap_quotes(obj))


def ensure_json_dumps(data):
    """
    This function hadles the case when the iam_role modules is used with the
    policies option which requiress a policy_document as a string. We'll need
    to ensure the correct quotes are used for the API call
    For example:
    'Policies': [{
        'PolicyName': 'dr-lambda-policy',
        'PolicyDocument': "{'Version': '2012-10-17', \
            'Statement': [{'Effect': 'Allow', \
                'Action': ['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents'], \
                    'Resource': 'arn:aws:logs:*:*:*'}, {'Effect': 'Allow', \
                        'Action': 'lambda:InvokeFunction', 'Resource': '*'}]}"
    }],
    will become:
    '"Policies": [{"PolicyName": "dr-lambda-policy", "PolicyDocument": "{\\"Version\\": \\"2012-10-17\\", \
                \\"Statement\\": [{\\"Effect\\": \\"Allow\\", \\"Action\\": [\\"logs:CreateLogGroup\\", \
                \\"logs:CreateLogStream\\", \\"logs:PutLogEvents\\"], \\"Resource\\": \\"arn:aws:logs:*:*:*\\"}, \
                {\\"Effect\\": \\"Allow\\", \\"Action\\": \\"lambda:InvokeFunction\\", \\"Resource\\": \\"*\\"}]}"}]'
    """

    if "Policies" in data and isinstance(data.get("Policies"), list):
        for policy_entry in data["Policies"]:
            if "PolicyDocument" in policy_entry and isinstance(
                policy_entry.get("PolicyDocument"), str
            ):
                inner_json = json.loads(
                    policy_entry["PolicyDocument"].replace("'", '"')
                )  # Convert single quotes to double quotes
                policy_entry["PolicyDocument"] = json.loads(
                    json.dumps(inner_json, cls=QuoteSwappingEncoder)
                )

    return data


def make_op(path, old, new, strategy):
    _new_cpy = copy.deepcopy(new)

    if isinstance(old, dict):
        if strategy == "merge":
            _new_cpy = dict(old, **new)
    elif isinstance(old, list):
        if strategy == "merge":
            _old_cpy = copy.deepcopy(old)
            if path == "Tags":
                _new_cpy = tag_merge(_old_cpy, new)
            else:
                # When list of dictionaries different with keys different that Key and values than Value need to be merged
                _new_cpy = merge_list_of_dicts(_old_cpy, new)

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
