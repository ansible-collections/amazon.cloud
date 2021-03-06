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
module: rdsdb_proxy
short_description: Create and manage DB proxies
description: Creates and manage DB proxies (list, create, update, describe, delete).
options:
    auth:
        description:
        - The authorization mechanism that the proxy uses.
        elements: dict
        required: true
        suboptions:
            auth_scheme:
                choices:
                - SECRETS
                description:
                - The type of authentication that the proxy uses for connections from
                    the proxy to the underlying database.
                type: str
            description:
                description:
                - A user-specified description about the authentication used by a
                    proxy to log in as a specific database user.
                type: str
            iam_auth:
                choices:
                - DISABLED
                - REQUIRED
                description:
                - Whether to require or disallow AWS Identity and Access Management
                    (IAM) authentication for connections to the proxy.
                type: str
            secret_arn:
                description:
                - The Amazon Resource Name (ARN) representing the secret that the
                    proxy uses to authenticate to the RDS DB instance or Aurora DB
                    cluster.
                - These secrets are stored within Amazon Secrets Manager.
                type: str
            user_name:
                description:
                - The name of the database user to which the proxy connects.
                type: str
        type: list
    db_proxy_name:
        description:
        - The identifier for the proxy.
        - This name must be unique for all proxies owned by your AWS account in the
            specified AWS Region.
        required: true
        type: str
    debug_logging:
        description:
        - Whether the proxy includes detailed information about SQL statements in
            its logs.
        type: bool
    engine_family:
        choices:
        - MYSQL
        - POSTGRESQL
        description:
        - The kinds of databases that the proxy can connect to.
        required: true
        type: str
    idle_client_timeout:
        description:
        - The number of seconds that a connection to the proxy can be inactive before
            the proxy disconnects it.
        type: int
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        required: false
        type: bool
    require_tls:
        description:
        - A Boolean parameter that specifies whether Transport Layer Security (TLS)
            encryption is required for connections to the proxy.
        type: bool
    role_arn:
        description:
        - The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access
            secrets in AWS Secrets Manager.
        required: true
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
    tags:
        aliases:
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        required: false
        type: dict
    vpc_security_group_ids:
        description:
        - VPC security group IDs to associate with the new proxy.
        elements: str
        type: list
    vpc_subnet_ids:
        description:
        - VPC subnet IDs to associate with the new proxy.
        elements: str
        required: true
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

    argument_spec["auth"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "auth_scheme": {"type": "str", "choices": ["SECRETS"]},
            "description": {"type": "str"},
            "iam_auth": {"type": "str", "choices": ["DISABLED", "REQUIRED"]},
            "secret_arn": {"type": "str"},
            "user_name": {"type": "str"},
        },
        "required": True,
    }
    argument_spec["db_proxy_name"] = {"type": "str", "required": True}
    argument_spec["debug_logging"] = {"type": "bool"}
    argument_spec["engine_family"] = {
        "type": "str",
        "choices": ["MYSQL", "POSTGRESQL"],
        "required": True,
    }
    argument_spec["idle_client_timeout"] = {"type": "int"}
    argument_spec["require_tls"] = {"type": "bool"}
    argument_spec["role_arn"] = {"type": "str", "required": True}
    argument_spec["tags"] = {
        "type": "dict",
        "required": False,
        "aliases": ["resource_tags"],
    }
    argument_spec["vpc_security_group_ids"] = {"type": "list", "elements": "str"}
    argument_spec["vpc_subnet_ids"] = {
        "type": "list",
        "elements": "str",
        "required": True,
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
        [
            "state",
            "present",
            ["role_arn", "db_proxy_name", "engine_family", "auth", "vpc_subnet_ids"],
            True,
        ],
        ["state", "absent", ["db_proxy_name"], True],
        ["state", "get", ["db_proxy_name"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::RDS::DBProxy"

    params = {}

    params["auth"] = module.params.get("auth")
    params["db_proxy_name"] = module.params.get("db_proxy_name")
    params["debug_logging"] = module.params.get("debug_logging")
    params["engine_family"] = module.params.get("engine_family")
    params["idle_client_timeout"] = module.params.get("idle_client_timeout")
    params["require_tls"] = module.params.get("require_tls")
    params["role_arn"] = module.params.get("role_arn")
    params["tags"] = module.params.get("tags")
    params["vpc_security_group_ids"] = module.params.get("vpc_security_group_ids")
    params["vpc_subnet_ids"] = module.params.get("vpc_subnet_ids")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags", None):
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["db_proxy_name", "engine_family", "vpc_subnet_ids"]

    state = module.params.get("state")
    identifier = module.params.get("db_proxy_name")

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
