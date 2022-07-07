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
module: redshift_event_subscription
short_description: Create and manage Amazon Redshift event notification subscriptions
description: Creates and manage Amazon Redshift event notification subscriptions (list,
    create, update, describe, delete).
options:
    enabled:
        description:
        - A boolean value; set to true to activate the subscription, and set to false
            to create the subscription but not activate it.
        type: bool
    event_categories:
        choices:
        - configuration
        - management
        - monitoring
        - pending
        - security
        description:
        - Specifies the Amazon Redshift event categories to be published by the event
            notification subscription.
        elements: str
        type: list
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        required: false
        type: bool
    severity:
        choices:
        - ERROR
        - INFO
        description:
        - Specifies the Amazon Redshift event severity to be published by the event
            notification subscription.
        type: str
    sns_topic_arn:
        description:
        - The Amazon Resource Name (ARN) of the Amazon SNS topic used to transmit
            the event notifications.
        type: str
    source_ids:
        description:
        - A list of one or more identifiers of Amazon Redshift source objects.
        elements: str
        type: list
    source_type:
        choices:
        - cluster
        - cluster-parameter-group
        - cluster-security-group
        - cluster-snapshot
        - scheduled-action
        description:
        - The type of source that will be generating the events.
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
    subscription_name:
        description:
        - The name of the Amazon Redshift event notification subscription
        required: true
        type: str
    tags:
        aliases:
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        required: false
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
version_added: 0.1.0
requirements: []
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
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

    argument_spec["subscription_name"] = {"type": "str", "required": True}
    argument_spec["sns_topic_arn"] = {"type": "str"}
    argument_spec["source_type"] = {
        "type": "str",
        "choices": [
            "cluster",
            "cluster-parameter-group",
            "cluster-security-group",
            "cluster-snapshot",
            "scheduled-action",
        ],
    }
    argument_spec["source_ids"] = {"type": "list", "elements": "str"}
    argument_spec["event_categories"] = {
        "type": "list",
        "elements": "str",
        "choices": ["configuration", "management", "monitoring", "pending", "security"],
    }
    argument_spec["severity"] = {"type": "str", "choices": ["ERROR", "INFO"]}
    argument_spec["enabled"] = {"type": "bool"}
    argument_spec["tags"] = {
        "type": "dict",
        "required": False,
        "aliases": ["resource_tags"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["purge_tags"] = {"type": "bool", "required": False, "default": True}

    required_if = [
        ["state", "present", ["subscription_name"], True],
        ["state", "absent", ["subscription_name"], True],
        ["state", "get", ["subscription_name"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Redshift::EventSubscription"

    params = {}

    params["enabled"] = module.params.get("enabled")
    params["event_categories"] = module.params.get("event_categories")
    params["severity"] = module.params.get("severity")
    params["sns_topic_arn"] = module.params.get("sns_topic_arn")
    params["source_ids"] = module.params.get("source_ids")
    params["source_type"] = module.params.get("source_type")
    params["subscription_name"] = module.params.get("subscription_name")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags", None):
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["subscription_name"]

    state = module.params.get("state")
    identifier = module.params.get("subscription_name")

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
