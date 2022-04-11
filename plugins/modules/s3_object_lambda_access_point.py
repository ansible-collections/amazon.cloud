#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by amazon_cloud_code_generator.
# See: https://github.com/ansible-collections/amazon_cloud_code_generator

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: s3_object_lambda_access_point
short_description: Create and manage Object Lambda Access Points used to access S3
    buckets
description: Create and manage Object Lambda Access Points used to access S3 buckets
    (list, create, update, describe, delete).
options:
    name:
        description:
        - The name you want to assign to this Object lambda Access Point.
        type: str
    object_lambda_configuration:
        description:
        - The Object lambda Access Point Configuration that configures transformations
            to be applied on the objects on specified S3 I(actions_configuration)
            to be applied to this Object lambda Access Point.
        - It specifies Supporting Access Point, Transformation Configurations.
        - Customers can also set if they like to enable Cloudwatch metrics for accesses
            to this Object lambda Access Point.
        - Default setting for Cloudwatch metrics is disable.
        required: true
        suboptions:
            allowed_features:
                description:
                - Not Provived.
                elements: str
                type: list
            cloud_watch_metrics_enabled:
                description:
                - Not Provived.
                type: bool
            supporting_access_point:
                description:
                - Not Provived.
                required: true
                type: str
            transformation_configurations:
                description:
                - Configuration to define what content transformation will be applied
                    on which S3 Action.
                elements: dict
                suboptions:
                    actions:
                        description:
                        - Not Provived.
                        elements: str
                        required: true
                        type: list
                    content_transformation:
                        description:
                        - Not Provived.
                        required: true
                        suboptions:
                            aws_lambda:
                                description:
                                - Not Provived.
                                suboptions:
                                    function_arn:
                                        description:
                                        - Not Provived.
                                        required: true
                                        type: str
                                    function_payload:
                                        description:
                                        - Not Provived.
                                        type: str
                                type: dict
                        type: dict
                type: list
        type: dict
    state:
        choices:
        - present
        - absent
        - list
        - describe
        - get
        default: present
        description:
        - Goal state for resource.
        - I(state=present) creates the resource if it doesn't exist, or updates to
            the provided state if the resource already exists.
        - I(state=absent) ensures an existing instance is deleted.
        - I(state=list) get all the existing resources.
        - I(state=describe) or I(state=get) retrieves information on an existing resource.
        type: str
    wait:
        default: false
        description:
        - Wait for operation to complete before returning.
        type: bool
    wait_timeout:
        default: 320
        description:
        - How many seconds to wait for an operation to complete before timing out.
        type: int
author: Ansible Cloud Team (@ansible-collections)
version_added: 0.1.0
requirements: []
extends_documentation_fragment:
- amazon.cloud.aws
- amazon.cloud.ec2
"""

EXAMPLES = r"""
"""

RETURN = r"""
result:
    description: Dictionary containing resource information.
    returned: always
    type: complex
    contains:
        identifier:
            description: The unique identifier of the resource.
            type: str
        properties:
            description: The resource properties.
            type: dict
"""

import json

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    CloudControlResource,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    snake_dict_to_camel_dict,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    ansible_dict_to_boto3_tag_list,
)


def main():

    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["name"] = {"type": "str"}
    argument_spec["object_lambda_configuration"] = {
        "type": "dict",
        "options": {
            "supporting_access_point": {"type": "str", "required": True},
            "allowed_features": {"type": "list", "elements": "str"},
            "cloud_watch_metrics_enabled": {"type": "bool"},
            "transformation_configurations": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "actions": {"type": "list", "required": True, "elements": "str"},
                    "content_transformation": {
                        "type": "dict",
                        "options": {
                            "aws_lambda": {
                                "type": "dict",
                                "options": {
                                    "function_arn": {"type": "str", "required": True},
                                    "function_payload": {"type": "str"},
                                },
                            }
                        },
                        "required": True,
                    },
                },
            },
        },
        "required": True,
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}

    required_if = [
        ["state", "present", ["name", "object_lambda_configuration"], True],
        ["state", "absent", ["name"], True],
        ["state", "get", ["name"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::S3ObjectLambda::AccessPoint"

    params = {}

    params["name"] = module.params.get("name")
    params["object_lambda_configuration"] = module.params.get(
        "object_lambda_configuration"
    )

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags", None):
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["name"]

    state = module.params.get("state")
    identifier = module.params.get("name")

    results = {"changed": False, "result": []}

    if state == "list":
        results["result"] = cloud.list_resources(type_name)

    if state in ("describe", "get"):
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "present":
        results["changed"] |= cloud.present(
            type_name, identifier, params_to_set, create_only_params
        )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "absent":
        results["changed"] |= cloud.absent(type_name, identifier)

    module.exit_json(**results)


if __name__ == "__main__":
    main()
