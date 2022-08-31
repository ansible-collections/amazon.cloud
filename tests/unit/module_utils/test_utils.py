# (c) 2021 Red Hat Inc.
#
# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.amazon.cloud.plugins.module_utils.utils import (
    ansible_dict_to_boto3_tag_list,
    boto3_tag_list_to_ansible_dict,
    diff_dicts,
    normalize_response,
    tag_merge,
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


def test_diff_empty_dicts_no_diff():
    a_dict = {}
    b_dict = {}
    match, diff = diff_dicts(a_dict, b_dict)

    assert match is True
    assert diff == {}


def test_diff_no_diff():
    a_dict = {
        "section1": {"category1": 1, "category2": 2},
        "section2": {
            "category1": 1,
            "category2": 2,
            "category4": {"foo_1": 1, "foo_2": {"bar_1": [1]}},
        },
        "section3": ["elem1", "elem2", "elem3"],
        "section4": ["Foo"],
    }
    match, diff = diff_dicts(a_dict, a_dict)

    assert match is True
    assert diff == {}


def test_diff_no_addition():
    a_dict = {
        "section1": {"category1": 1, "category2": 2},
        "section2": {
            "category1": 1,
            "category2": 2,
            "category4": {"foo_1": 1, "foo_2": {"bar_1": [1]}},
        },
        "section3": ["elem3", "elem1", "elem2"],
        "section4": ["Bar"],
    }
    b_dict = {
        "section1": {"category1": 1, "category2": 2},
        "section2": {
            "category1": 1,
            "category2": 3,
            "category4": {"foo_1": 1, "foo_2": {"bar_1": [1]}},
        },
        "section3": ["elem3", "elem1", "elem2"],
        "section4": ["Foo"],
    }

    match, diff = diff_dicts(a_dict, b_dict)

    assert match is False
    assert diff["before"] == {"section4": ["Bar"], "section2": {"category2": 2}}
    assert diff["after"] == {"section4": ["Foo"], "section2": {"category2": 3}}


def test_diff_with_addition():
    a_dict = {
        "section1": {"category1": 1, "category2": 2},
        "section2": {
            "category1": 1,
            "category2": 2,
            "category4": {"foo_1": 1, "foo_2": {"bar_1": [1]}},
        },
        "section3": ["elem3", "elem1", "elem2"],
        "section4": ["Bar"],
    }
    b_dict = {
        "section1": {"category1": 1, "category2": 2},
        "section2": {
            "category1": 1,
            "category2": 2,
            "category4": {"foo_1": 1, "foo_2": {"bar_1": [1]}},
        },
        "section3": ["elem3", "elem1", "elem2"],
        "section4": ["Foo", "Bar"],
        "section5": ["FooBar"],
    }
    match, diff = diff_dicts(a_dict, b_dict)

    assert match is False
    assert diff["before"] == {"section4": ["Bar"]}
    assert diff["after"] == {"section5": ["FooBar"], "section4": ["Foo", "Bar"]}


def test_normalize_response_single():
    response = {
        "ResourceDescription": {
            "Identifier": "test_one",
            "Properties": '{"BucketName":"test_one","RegionalDomainName":"test_one.s3.us-east-1.amazonaws.com", \
            "DomainName":"test_one.s3.amazonaws.com","WebsiteURL":"http://test_one.s3-website-us-east-1.amazonaws.com", \
            "DualStackDomainName":"test_one.s3.dualstack.us-east-1.amazonaws.com", \
            "Arn":"arn:aws:s3:::test_one","Tags":[{"Value":"pascalCaseValue","Key":"newPascalCaseKey"}, \
            {"Value":"CamelCaseValue","Key":"NewCamelCaseKey"},{"Value":"snake_case_value","Key":"new_snake_case_key"}, \
            {"Value":"Value with spaces","Key":"New Key with Spaces"}]}',
        }
    }
    normalized_response = {
        "identifier": "test_one",
        "properties": {
            "bucket_name": "test_one",
            "regional_domain_name": "test_one.s3.us-east-1.amazonaws.com",
            "domain_name": "test_one.s3.amazonaws.com",
            "website_url": "http://test_one.s3-website-us-east-1.amazonaws.com",
            "dual_stack_domain_name": "test_one.s3.dualstack.us-east-1.amazonaws.com",
            "arn": "arn:aws:s3:::test_one",
            "tags": {
                "newPascalCaseKey": "pascalCaseValue",
                "NewCamelCaseKey": "CamelCaseValue",
                "new_snake_case_key": "snake_case_value",
                "New Key with Spaces": "Value with spaces",
            },
        },
    }
    assert normalized_response == normalize_response(response)


def test_normalize_response_multiple():
    response = {
        "ResourceDescriptions": [
            {
                "Identifier": "test_one",
                "Properties": '{"BucketName":"test_one","RegionalDomainName":"test_one.s3.us-east-1.amazonaws.com", \
                "DomainName":"test_one.s3.amazonaws.com","WebsiteURL":"http://test_one.s3-website-us-east-1.amazonaws.com", \
                "DualStackDomainName":"test_one.s3.dualstack.us-east-1.amazonaws.com", \
                "Arn":"arn:aws:s3:::test_one","Tags":[{"Value":"pascalCaseValue","Key":"newPascalCaseKey"}, \
                {"Value":"CamelCaseValue","Key":"NewCamelCaseKey"},{"Value":"snake_case_value","Key":"new_snake_case_key"}, \
                {"Value":"Value with spaces","Key":"New Key with Spaces"}]}',
            },
            {
                "Identifier": "test_two",
                "Properties": '{"BucketName":"test_two","RegionalDomainName":"test_two.s3.us-east-1.amazonaws.com", \
                "DomainName":"test_two.s3.amazonaws.com","WebsiteURL":"http://test_two.s3-website-us-east-1.amazonaws.com", \
                "DualStackDomainName":"test_two.s3.dualstack.us-east-1.amazonaws.com", \
                "Arn":"arn:aws:s3:::test_two","Tags":[{"Value":"pascalCaseValue","Key":"newPascalCaseKey"}, \
                {"Value":"CamelCaseValue","Key":"NewCamelCaseKey"},{"Value":"snake_case_value","Key":"new_snake_case_key"}, \
                {"Value":"Value with spaces","Key":"New Key with Spaces"}]}',
            },
        ]
    }
    normalized_response = [
        {
            "identifier": "test_one",
            "properties": {
                "bucket_name": "test_one",
                "regional_domain_name": "test_one.s3.us-east-1.amazonaws.com",
                "domain_name": "test_one.s3.amazonaws.com",
                "website_url": "http://test_one.s3-website-us-east-1.amazonaws.com",
                "dual_stack_domain_name": "test_one.s3.dualstack.us-east-1.amazonaws.com",
                "arn": "arn:aws:s3:::test_one",
                "tags": {
                    "newPascalCaseKey": "pascalCaseValue",
                    "NewCamelCaseKey": "CamelCaseValue",
                    "new_snake_case_key": "snake_case_value",
                    "New Key with Spaces": "Value with spaces",
                },
            },
        },
        {
            "identifier": "test_two",
            "properties": {
                "bucket_name": "test_two",
                "regional_domain_name": "test_two.s3.us-east-1.amazonaws.com",
                "domain_name": "test_two.s3.amazonaws.com",
                "website_url": "http://test_two.s3-website-us-east-1.amazonaws.com",
                "dual_stack_domain_name": "test_two.s3.dualstack.us-east-1.amazonaws.com",
                "arn": "arn:aws:s3:::test_two",
                "tags": {
                    "newPascalCaseKey": "pascalCaseValue",
                    "NewCamelCaseKey": "CamelCaseValue",
                    "new_snake_case_key": "snake_case_value",
                    "New Key with Spaces": "Value with spaces",
                },
            },
        },
    ]
    assert normalized_response == normalize_response(response)


def test_tag_merge_empty_dicts():
    dict_1 = []
    dict_2 = []
    expected = []

    tag_merge(dict_1, dict_2)
    assert dict_1 == expected


def test_tag_merge_one_empty_dict():
    dict_1 = []
    dict_2 = [
        {"Key": "newPascalCaseKey", "Value": "pascalCaseValue"},
        {"Key": "NewCamelCaseKey", "Value": "CamelCaseValue"},
        {"Key": "new_snake_case_key", "Value": "snake_case_value"},
        {"Key": "New Key with Spaces", "Value": "Updated Value with spaces"},
    ]

    expected = [
        {"Key": "newPascalCaseKey", "Value": "pascalCaseValue"},
        {"Key": "NewCamelCaseKey", "Value": "CamelCaseValue"},
        {"Key": "new_snake_case_key", "Value": "snake_case_value"},
        {"Key": "New Key with Spaces", "Value": "Updated Value with spaces"},
    ]

    tag_merge(dict_1, dict_2)
    assert dict_1 == expected


def test_tag_merge_dicts():
    dict_1 = [
        {"Key": "Key with Spaces", "Value": "Value with spaces"},
        {"Key": "CamelCaseKey", "Value": "CamelCaseValue"},
        {"Key": "pascalCaseKey", "Value": "pascalCaseValue"},
        {"Key": "snake_case_key", "Value": "snake_case_value"},
        {"Key": "New Key with Spaces", "Value": "Value with spaces"},
    ]

    dict_2 = [
        {"Key": "newPascalCaseKey", "Value": "pascalCaseValue"},
        {"Key": "NewCamelCaseKey", "Value": "CamelCaseValue"},
        {"Key": "new_snake_case_key", "Value": "snake_case_value"},
        {"Key": "New Key with Spaces", "Value": "Updated Value with spaces"},
    ]

    expected = [
        {"Key": "Key with Spaces", "Value": "Value with spaces"},
        {"Key": "CamelCaseKey", "Value": "CamelCaseValue"},
        {"Key": "pascalCaseKey", "Value": "pascalCaseValue"},
        {"Key": "snake_case_key", "Value": "snake_case_value"},
        {"Key": "New Key with Spaces", "Value": "Updated Value with spaces"},
        {"Key": "newPascalCaseKey", "Value": "pascalCaseValue"},
        {"Key": "NewCamelCaseKey", "Value": "CamelCaseValue"},
        {"Key": "new_snake_case_key", "Value": "snake_case_value"},
    ]

    tag_merge(dict_1, dict_2)
    assert dict_1 == expected
