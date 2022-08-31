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
module: redshift_scheduled_action
short_description: Creates and manages a scheduled action
description:
- Creates and manages a scheduled action.
- A scheduled action contains a schedule and an Amazon Redshift API action.
- For example, you can create a schedule of when to run the ResizeCluster API operation.
options:
    enable:
        description:
        - If true, the schedule is enabled.
        - If false, the scheduled action does not trigger.
        type: bool
    end_time:
        description:
        - The end time in UTC of the scheduled action.
        - After this time, the scheduled action does not trigger.
        type: str
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    iam_role:
        description:
        - The IAM role to assume to run the target action.
        type: str
    schedule:
        description:
        - The schedule in at( ) or cron( ) format.
        type: str
    scheduled_action_description:
        description:
        - The description of the scheduled action.
        type: str
    scheduled_action_name:
        description:
        - The name of the scheduled action.
        - The name must be unique within an account.
        type: str
    start_time:
        description:
        - The start time in UTC of the scheduled action.
        - Before this time, the scheduled action does not trigger.
        type: str
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
    target_action:
        description:
        - A JSON format string of the Amazon Redshift API operation with input parameters.
        suboptions:
            pause_cluster:
                description:
                - Describes a pause cluster operation.
                - For example, a scheduled action to run the I(pause_cluster) API
                    operation.
                suboptions:
                    cluster_identifier:
                        description:
                        - Not Provived.
                        type: str
                type: dict
            resize_cluster:
                description:
                - Describes a resize cluster operation.
                - For example, a scheduled action to run the I(resize_cluster) API
                    operation.
                suboptions:
                    classic:
                        description:
                        - Not Provived.
                        type: bool
                    cluster_identifier:
                        description:
                        - Not Provived.
                        type: str
                    cluster_type:
                        description:
                        - Not Provived.
                        type: str
                    node_type:
                        description:
                        - Not Provived.
                        type: str
                    number_of_nodes:
                        description:
                        - Not Provived.
                        type: int
                type: dict
            resume_cluster:
                description:
                - Describes a resume cluster operation.
                - For example, a scheduled action to run the I(resume_cluster) API
                    operation.
                suboptions:
                    cluster_identifier:
                        description:
                        - Not Provived.
                        type: str
                type: dict
        type: dict
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
version_added: 0.2.0
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
"""

EXAMPLES = r"""
"""

RETURN = r"""
result:
    description:
        - When I(state=list), it is a list containing dictionaries of resource information.
        - Otherwise, it is a dictionary of resource information.
        - When I(state=absent), it is an empty dictionary.
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

    argument_spec["scheduled_action_name"] = {"type": "str"}
    argument_spec["target_action"] = {
        "type": "dict",
        "options": {
            "resize_cluster": {
                "type": "dict",
                "options": {
                    "cluster_identifier": {"type": "str"},
                    "cluster_type": {"type": "str"},
                    "node_type": {"type": "str"},
                    "number_of_nodes": {"type": "int"},
                    "classic": {"type": "bool"},
                },
            },
            "pause_cluster": {
                "type": "dict",
                "options": {"cluster_identifier": {"type": "str"}},
            },
            "resume_cluster": {
                "type": "dict",
                "options": {"cluster_identifier": {"type": "str"}},
            },
        },
    }
    argument_spec["schedule"] = {"type": "str"}
    argument_spec["iam_role"] = {"type": "str"}
    argument_spec["scheduled_action_description"] = {"type": "str"}
    argument_spec["start_time"] = {"type": "str"}
    argument_spec["end_time"] = {"type": "str"}
    argument_spec["enable"] = {"type": "bool"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}

    required_if = [
        ["state", "present", ["scheduled_action_name"], True],
        ["state", "absent", ["scheduled_action_name"], True],
        ["state", "get", ["scheduled_action_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Redshift::ScheduledAction"

    params = {}

    params["enable"] = module.params.get("enable")
    params["end_time"] = module.params.get("end_time")
    params["iam_role"] = module.params.get("iam_role")
    params["schedule"] = module.params.get("schedule")
    params["scheduled_action_description"] = module.params.get(
        "scheduled_action_description"
    )
    params["scheduled_action_name"] = module.params.get("scheduled_action_name")
    params["start_time"] = module.params.get("start_time")
    params["target_action"] = module.params.get("target_action")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["scheduled_action_name"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["scheduled_action_name"]

    results = {"changed": False, "result": {}}

    if state == "list":
        if "list" not in handlers:
            module.exit_json(
                **results, msg=f"Resource type {type_name} cannot be listed."
            )
        results["result"] = cloud.list_resources(type_name, identifier)

    if state in ("describe", "get"):
        if "read" not in handlers:
            module.exit_json(
                **results, msg=f"Resource type {type_name} cannot be read."
            )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "present":
        results = cloud.present(
            type_name, identifier, params_to_set, create_only_params
        )

    if state == "absent":
        results["changed"] |= cloud.absent(type_name, identifier)

    module.exit_json(**results)


if __name__ == "__main__":
    main()
