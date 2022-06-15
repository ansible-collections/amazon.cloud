# (c) 2021 Red Hat Inc.
#
# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.amazon.cloud.plugins.module_utils.utils import (
    ansible_dict_to_boto3_tag_list,
    boto3_tag_list_to_ansible_dict,
    scrub_keys,
)


def test__ansible_dict_to_boto3_tag_list():
    tags_dict = {
        "lowerCamel": "lowerCamelValue",
        "UpperCamel": "upperCamelValue",
        "Normal case": "Normal Value",
        "lower case": "lower case value",
    }
    expected = [
        {"Key": "lowerCamel", "Value": "lowerCamelValue"},
        {"Key": "UpperCamel", "Value": "upperCamelValue"},
        {"Key": "Normal case", "Value": "Normal Value"},
        {"Key": "lower case", "Value": "lower case value"},
    ]
    converted_list = ansible_dict_to_boto3_tag_list(tags_dict)
    sorted_converted_list = sorted(converted_list, key=lambda i: (i["Key"]))
    sorted_list = sorted(expected, key=lambda i: (i["Key"]))
    assert sorted_converted_list == sorted_list


def test_boto3_tag_list_to_ansible_dict():
    tag_boto3_list = [
        {"Key": "lowerCamel", "Value": "lowerCamelValue"},
        {"Key": "UpperCamel", "Value": "upperCamelValue"},
        {"Key": "Normal case", "Value": "Normal Value"},
        {"Key": "lower case", "Value": "lower case value"},
    ]
    expected = {
        "lowerCamel": "lowerCamelValue",
        "UpperCamel": "upperCamelValue",
        "Normal case": "Normal Value",
        "lower case": "lower case value",
    }
    converted_dict = boto3_tag_list_to_ansible_dict(tag_boto3_list)
    assert converted_dict == expected


def test_boto3_tag_list_to_ansible_dict_empty():
    # AWS returns [] when there are no tags
    assert boto3_tag_list_to_ansible_dict([]) == {}
    # Minio returns [{}] when there are no tags
    assert boto3_tag_list_to_ansible_dict([{}]) == {}


def test_scrub_keys_empty_dict():
    dict = {}
    keys_to_remove = list(range(3))
    assert scrub_keys(dict, keys_to_remove) == dict


def test_scrub_keys_empty_keys_to_remove():
    dict = {i: i for i in range(10)}
    keys_to_remove = []
    assert scrub_keys(dict, keys_to_remove) == dict


def test_scrub_keys_remove_keys_not_in_dict():
    dict = {i: i for i in range(10)}
    keys_to_remove = [i for i in range(20) if i % 2 == 0]
    expected = {i: i for i in range(10) if i % 2 == 1}
    assert scrub_keys(dict, keys_to_remove) == expected


def test_scrub_keys_duplicate_keys():
    dict = {i: i for i in range(10)}
    keys_to_remove = [i for i in range(20) if i % 2 == 0] * 2
    expected = {i: i for i in range(10) if i % 2 == 1}
    assert scrub_keys(dict, keys_to_remove) == expected
