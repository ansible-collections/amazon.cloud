#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: autoscaling_lifecycle_hook
short_description: Creates and manages an Auto Scaling group
description:
- Creates and manages an Auto Scaling group.
- The AWS AutoScaling Lifecycle Hook resource specifies lifecycle hooks for an Auto
    Scaling group.
- These hooks let you create solutions that are aware of events in the Auto Scaling
    instance lifecycle, and then perform a custom action on instances when the corresponding
    lifecycle event occurs.
- A lifecycle hook provides a specified amount of time (one hour by default) to wait
    for the action to complete before the instance transitions to the next state.
options:
    auto_scaling_group_name:
        aliases:
        - AutoScalingGroupName
        description:
        - The name of the Auto Scaling group for the lifecycle hook.
        type: str
    default_result:
        aliases:
        - DefaultResult
        description:
        - The action the Auto Scaling group takes when the lifecycle hook timeout
            elapses or if an unexpected failure occurs.
        - The valid values are CONTINUE and ABANDON (default).
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
    heartbeat_timeout:
        aliases:
        - HeartbeatTimeout
        description:
        - The maximum time, in seconds, that can elapse before the lifecycle hook
            times out.
        - The range is from 30 to 7200 seconds.
        - The default value is 3600 seconds (1 hour).
        - If the lifecycle hook times out, Amazon EC2 Auto Scaling performs the action
            that you specified in the DefaultResult property.
        type: int
    identifier:
        description:
        - For compound primary identifiers, to specify the primary identifier as a
            string, list each in the order that they are specified in the identifier
            list definition, separated by '|'.
        - For more details, visit U(https://docs.aws.amazon.com/cloudcontrolapi/latest/userguide/resource-identifier.html).
        type: str
    lifecycle_hook_name:
        aliases:
        - LifecycleHookName
        description:
        - The name of the lifecycle hook.
        type: str
    lifecycle_transition:
        aliases:
        - LifecycleTransition
        description:
        - The instance state to which you want to attach the lifecycle hook.
        type: str
    notification_metadata:
        aliases:
        - NotificationMetadata
        description:
        - Additional information that is included any time Amazon EC2 Auto Scaling
            sends a message to the notification target.
        type: str
    notification_target_arn:
        aliases:
        - NotificationTargetARN
        description:
        - The Amazon Resource Name (ARN) of the notification target that Amazon EC2
            Auto Scaling uses to notify you when an instance is in the transition
            state for the lifecycle hook.
        - You can specify an Amazon SQS queue or an Amazon SNS topic.
        - 'The notification message includes the following information: lifecycle
            action token, user account ID, Auto Scaling group name, lifecycle hook
            name, instance ID, lifecycle transition, and notification metadata.'
        type: str
    role_arn:
        aliases:
        - RoleARN
        description:
        - The ARN of the IAM role that allows the Auto Scaling group to publish to
            the specified notification target, for example, an Amazon SNS topic or
            an Amazon SQS queue.
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
version_added: 0.3.0
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

    argument_spec["auto_scaling_group_name"] = {
        "type": "str",
        "aliases": ["AutoScalingGroupName"],
    }
    argument_spec["default_result"] = {"type": "str", "aliases": ["DefaultResult"]}
    argument_spec["heartbeat_timeout"] = {
        "type": "int",
        "aliases": ["HeartbeatTimeout"],
    }
    argument_spec["lifecycle_hook_name"] = {
        "type": "str",
        "aliases": ["LifecycleHookName"],
    }
    argument_spec["lifecycle_transition"] = {
        "type": "str",
        "aliases": ["LifecycleTransition"],
    }
    argument_spec["notification_metadata"] = {
        "type": "str",
        "aliases": ["NotificationMetadata"],
    }
    argument_spec["notification_target_arn"] = {
        "type": "str",
        "aliases": ["NotificationTargetARN"],
    }
    argument_spec["role_arn"] = {"type": "str", "aliases": ["RoleARN"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}
    argument_spec["identifier"] = {"type": "str"}

    required_if = [
        ["state", "list", ["auto_scaling_group_name"], True],
        [
            "state",
            "present",
            [
                "lifecycle_transition",
                "identifier",
                "lifecycle_hook_name",
                "auto_scaling_group_name",
            ],
            True,
        ],
        [
            "state",
            "absent",
            ["auto_scaling_group_name", "lifecycle_hook_name", "identifier"],
            True,
        ],
        [
            "state",
            "get",
            ["auto_scaling_group_name", "lifecycle_hook_name", "identifier"],
            True,
        ],
    ]
    mutually_exclusive = [
        [("auto_scaling_group_name", "lifecycle_hook_name"), "identifier"]
    ]

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::AutoScaling::LifecycleHook"

    params = {}

    params["auto_scaling_group_name"] = module.params.get("auto_scaling_group_name")
    params["default_result"] = module.params.get("default_result")
    params["heartbeat_timeout"] = module.params.get("heartbeat_timeout")
    params["identifier"] = module.params.get("identifier")
    params["lifecycle_hook_name"] = module.params.get("lifecycle_hook_name")
    params["lifecycle_transition"] = module.params.get("lifecycle_transition")
    params["notification_metadata"] = module.params.get("notification_metadata")
    params["notification_target_arn"] = module.params.get("notification_target_arn")
    params["role_arn"] = module.params.get("role_arn")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/AutoScalingGroupName",
        "/properties/LifecycleHookName",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/AutoScalingGroupName", "/properties/LifecycleHookName"]
    if (
        state in ("present", "absent", "get", "describe")
        and module.params.get("identifier") is None
    ):
        if not module.params.get("auto_scaling_group_name") or not module.params.get(
            "lifecycle_hook_name"
        ):
            module.fail_json(
                "You must specify all the ('auto_scaling_group_name', 'lifecycle_hook_name') identifiers."
            )

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
