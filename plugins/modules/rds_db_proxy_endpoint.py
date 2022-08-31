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
module: rds_db_proxy_endpoint
short_description: Creates and manages a DB proxy endpoint
description:
- Creates and manages a DB proxy endpoint.
- You can use custom proxy endpoints to access a proxy through a different VPC than
    the proxy's default VPC.
options:
    db_proxy_endpoint_name:
        description:
        - The identifier for the DB proxy endpoint.
        - This name must be unique for all DB proxy endpoints owned by your AWS account
            in the specified AWS Region.
        type: str
    db_proxy_name:
        description:
        - The identifier for the proxy.
        - This name must be unique for all proxies owned by your AWS account in the
            specified AWS Region.
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
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        type: dict
    target_role:
        choices:
        - READ_ONLY
        - READ_WRITE
        description:
        - A value that indicates whether the DB proxy endpoint can be used for read/write
            or read-only operations.
        type: str
    vpc_security_group_ids:
        description:
        - VPC security group IDs to associate with the new DB proxy endpoint.
        elements: str
        type: list
    vpc_subnet_ids:
        description:
        - VPC subnet IDs to associate with the new DB proxy endpoint.
        elements: str
        type: list
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

    argument_spec["db_proxy_endpoint_name"] = {"type": "str"}
    argument_spec["db_proxy_name"] = {"type": "str"}
    argument_spec["vpc_security_group_ids"] = {"type": "list", "elements": "str"}
    argument_spec["vpc_subnet_ids"] = {"type": "list", "elements": "str"}
    argument_spec["target_role"] = {
        "type": "str",
        "choices": ["READ_ONLY", "READ_WRITE"],
    }
    argument_spec["tags"] = {"type": "dict", "aliases": ["resource_tags"]}
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
        [
            "state",
            "present",
            ["db_proxy_endpoint_name", "vpc_subnet_ids", "db_proxy_name"],
            True,
        ],
        ["state", "absent", ["db_proxy_endpoint_name"], True],
        ["state", "get", ["db_proxy_endpoint_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::RDS::DBProxyEndpoint"

    params = {}

    params["db_proxy_endpoint_name"] = module.params.get("db_proxy_endpoint_name")
    params["db_proxy_name"] = module.params.get("db_proxy_name")
    params["tags"] = module.params.get("tags")
    params["target_role"] = module.params.get("target_role")
    params["vpc_security_group_ids"] = module.params.get("vpc_security_group_ids")
    params["vpc_subnet_ids"] = module.params.get("vpc_subnet_ids")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "db_proxy_name",
        "db_proxy_endpoint_name",
        "vpc_subnet_ids",
        "target_role",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["db_proxy_endpoint_name"]

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
