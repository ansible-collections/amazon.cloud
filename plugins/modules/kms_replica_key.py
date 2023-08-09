#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: kms_replica_key
short_description: Creates and manages a multi-Region replica key that is based on
    a multi-Region primary key
description:
- Creates andn manages a multi-Region replica key that is based on a multi-Region
    primary key.
options:
    description:
        aliases:
        - Description
        description:
        - A description of the AWS KMS key.
        - Use a description that helps you to distinguish this AWS KMS key from others
            in the account, such as its intended use.
        type: str
    enabled:
        aliases:
        - Enabled
        description:
        - Specifies whether the AWS KMS key is enabled.
        - Disabled AWS KMS keys cannot be used in cryptographic operations.
        type: bool
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    key_policy:
        aliases:
        - KeyPolicy
        description:
        - The key policy that authorizes use of the AWS KMS key.
        - The key policy must observe the following rules.
        type: dict
    pending_window_in_days:
        aliases:
        - PendingWindowInDays
        description:
        - Specifies the number of days in the waiting period before AWS KMS deletes
            an AWS KMS key that has been removed from a CloudFormation stack.
        - Enter a value between 7 and 30 days.
        - The default value is 30 days.
        type: int
    primary_key_arn:
        aliases:
        - PrimaryKeyArn
        description:
        - Identifies the primary AWS KMS key to create a replica of.
        - Specify the Amazon Resource Name (ARN) of the AWS KMS key.
        - You cannot specify an alias or key ID. For help finding the ARN, see Finding
            the Key ID and ARN in the AWS Key Management Service Developer Guide.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
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
version_added: 0.2.0
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
from ansible_collections.amazon.cloud.plugins.module_utils.core import camel_to_snake


def main():
    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["primary_key_arn"] = {"type": "str", "aliases": ["PrimaryKeyArn"]}
    argument_spec["description"] = {"type": "str", "aliases": ["Description"]}
    argument_spec["enabled"] = {"type": "bool", "aliases": ["Enabled"]}
    argument_spec["key_policy"] = {"type": "dict", "aliases": ["KeyPolicy"]}
    argument_spec["pending_window_in_days"] = {
        "type": "int",
        "aliases": ["PendingWindowInDays"],
    }
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
        ["state", "present", ["key_policy", "primary_key_arn", "key_id"], True],
        ["state", "absent", ["key_id"], True],
        ["state", "get", ["key_id"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::KMS::ReplicaKey"

    params = {}

    params["description"] = module.params.get("description")
    params["enabled"] = module.params.get("enabled")
    params["key_policy"] = module.params.get("key_policy")
    params["pending_window_in_days"] = module.params.get("pending_window_in_days")
    params["primary_key_arn"] = module.params.get("primary_key_arn")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["/properties/PrimaryKeyArn"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/KeyId"]

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
