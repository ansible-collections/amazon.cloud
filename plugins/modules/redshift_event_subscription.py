#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: redshift_event_subscription
short_description: Create and manage Amazon Redshift event notification subscriptions
description:
- Creates and manage Amazon Redshift event notification subscriptions.
options:
    enabled:
        aliases:
        - Enabled
        description:
        - A boolean value; set to true to activate the subscription, and set to false
            to create the subscription but not activate it.
        type: bool
    event_categories:
        aliases:
        - EventCategories
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
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    severity:
        aliases:
        - Severity
        choices:
        - ERROR
        - INFO
        description:
        - Specifies the Amazon Redshift event severity to be published by the event
            notification subscription.
        type: str
    sns_topic_arn:
        aliases:
        - SnsTopicArn
        description:
        - The Amazon Resource Name (ARN) of the Amazon SNS topic used to transmit
            the event notifications.
        type: str
    source_ids:
        aliases:
        - SourceIds
        description:
        - A list of one or more identifiers of Amazon Redshift source objects.
        elements: str
        type: list
    source_type:
        aliases:
        - SourceType
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
        aliases:
        - SubscriptionName
        description:
        - The name of the Amazon Redshift event notification subscription.
        type: str
    tags:
        aliases:
        - Tags
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
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
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
- amazon.cloud.boto3
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


from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    AnsibleAmazonCloudModule,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    CloudControlResource,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    ansible_dict_to_boto3_tag_list,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    scrub_none_parameters,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import map_key_to_alias


def main():
    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["subscription_name"] = {
        "type": "str",
        "aliases": ["SubscriptionName"],
    }
    argument_spec["sns_topic_arn"] = {"type": "str", "aliases": ["SnsTopicArn"]}
    argument_spec["source_type"] = {
        "type": "str",
        "choices": [
            "cluster",
            "cluster-parameter-group",
            "cluster-security-group",
            "cluster-snapshot",
            "scheduled-action",
        ],
        "aliases": ["SourceType"],
    }
    argument_spec["source_ids"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["SourceIds"],
    }
    argument_spec["event_categories"] = {
        "type": "list",
        "elements": "str",
        "choices": ["configuration", "management", "monitoring", "pending", "security"],
        "aliases": ["EventCategories"],
    }
    argument_spec["severity"] = {
        "type": "str",
        "choices": ["ERROR", "INFO"],
        "aliases": ["Severity"],
    }
    argument_spec["enabled"] = {"type": "bool", "aliases": ["Enabled"]}
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags", "resource_tags"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}
    argument_spec["purge_tags"] = {"type": "bool", "default": True}

    required_if = [
        ["state", "present", ["subscription_name"], True],
        ["state", "absent", ["subscription_name"], True],
        ["state", "get", ["subscription_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
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
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["/properties/SubscriptionName"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/SubscriptionName"]

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
