#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: route53_key_signing_key
short_description: Creates a new key-signing key (KSK) in a hosted zone
description:
- Creates a new key-signing key (KSK) in a hosted zone.
options:
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    hosted_zone_id:
        aliases:
        - HostedZoneId
        description:
        - The unique string (ID) used to identify a hosted zone.
        type: str
    identifier:
        description:
        - For compound primary identifiers, to specify the primary identifier as a
            string, list each in the order that they are specified in the identifier
            list definition, separated by '|'.
        - For more details, visit U(https://docs.aws.amazon.com/cloudcontrolapi/latest/userguide/resource-identifier.html).
        type: str
    key_management_service_arn:
        aliases:
        - KeyManagementServiceArn
        description:
        - The Amazon resource name (ARN) for a customer managed key (CMK) in AWS Key
            Management Service (KMS). The KeyManagementServiceArn must be unique for
            each key signing key (KSK) in a single hosted zone.
        type: str
    name:
        aliases:
        - Name
        description:
        - An alphanumeric string used to identify a key signing key (KSK). Name must
            be unique for each key signing key in the same hosted zone.
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
    status:
        aliases:
        - Status
        choices:
        - ACTIVE
        - INACTIVE
        description:
        - A string specifying the initial status of the key signing key (KSK). You
            can set the value to ACTIVE or INACTIVE.
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


def main():
    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["hosted_zone_id"] = {"type": "str", "aliases": ["HostedZoneId"]}
    argument_spec["status"] = {
        "type": "str",
        "choices": ["ACTIVE", "INACTIVE"],
        "aliases": ["Status"],
    }
    argument_spec["name"] = {"type": "str", "aliases": ["Name"]}
    argument_spec["key_management_service_arn"] = {
        "type": "str",
        "aliases": ["KeyManagementServiceArn"],
    }
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
        ["state", "list", ["hosted_zone_id"], True],
        [
            "state",
            "present",
            [
                "hosted_zone_id",
                "name",
                "key_management_service_arn",
                "status",
                "identifier",
            ],
            True,
        ],
        ["state", "absent", ["hosted_zone_id", "name", "identifier"], True],
        ["state", "get", ["hosted_zone_id", "name", "identifier"], True],
    ]
    mutually_exclusive = [[("hosted_zone_id", "name"), "identifier"]]

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Route53::KeySigningKey"

    params = {}

    params["hosted_zone_id"] = module.params.get("hosted_zone_id")
    params["identifier"] = module.params.get("identifier")
    params["key_management_service_arn"] = module.params.get(
        "key_management_service_arn"
    )
    params["name"] = module.params.get("name")
    params["status"] = module.params.get("status")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/HostedZoneId",
        "/properties/Name",
        "/properties/KeyManagementServiceArn",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/HostedZoneId", "/properties/Name"]
    if (
        state in ("present", "absent", "get", "describe")
        and module.params.get("identifier") is None
    ):
        if not module.params.get("hosted_zone_id") or not module.params.get("name"):
            module.fail_json(
                "You must specify all the ('hosted_zone_id', 'name') identifiers."
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
