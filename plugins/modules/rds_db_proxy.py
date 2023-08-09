#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: rds_db_proxy
short_description: Create and manage DB proxies
description:
- Creates and manage DB proxies.
options:
    auth:
        aliases:
        - Auth
        description:
        - The authorization mechanism that the proxy uses.
        elements: dict
        suboptions:
            auth_scheme:
                aliases:
                - AuthScheme
                choices:
                - SECRETS
                description:
                - The type of authentication that the proxy uses for connections from
                    the proxy to the underlying database.
                type: str
            client_password_auth_type:
                aliases:
                - ClientPasswordAuthType
                choices:
                - MYSQL_NATIVE_PASSWORD
                - POSTGRES_MD5
                - POSTGRES_SCRAM_SHA_256
                - SQL_SERVER_AUTHENTICATION
                description:
                - The type of authentication the proxy uses for connections from clients.
                type: str
            description:
                aliases:
                - Description
                description:
                - A user-specified description about the authentication used by a
                    proxy to log in as a specific database user.
                type: str
            iam_auth:
                aliases:
                - IAMAuth
                choices:
                - DISABLED
                - ENABLED
                - REQUIRED
                description:
                - Whether to require or disallow Amazon Web Services Identity and
                    Access Management (IAM) authentication for connections to the
                    proxy.
                - The C(ENABLED) value is valid only for proxies with RDS for Microsoft
                    SQL Server.
                type: str
            secret_arn:
                aliases:
                - SecretArn
                description:
                - The Amazon Resource Name (ARN) representing the secret that the
                    proxy uses to authenticate to the RDS DB instance or Aurora DB
                    cluster.
                - These secrets are stored within Amazon Secrets Manager.
                type: str
        type: list
    db_proxy_name:
        aliases:
        - DBProxyName
        description:
        - The identifier for the proxy.
        - This name must be unique for all proxies owned by your AWS account in the
            specified AWS Region.
        type: str
    debug_logging:
        aliases:
        - DebugLogging
        description:
        - Whether the proxy includes detailed information about SQL statements in
            its logs.
        type: bool
    engine_family:
        aliases:
        - EngineFamily
        choices:
        - MYSQL
        - POSTGRESQL
        - SQLSERVER
        description:
        - The kinds of databases that the proxy can connect to.
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
    idle_client_timeout:
        aliases:
        - IdleClientTimeout
        description:
        - The number of seconds that a connection to the proxy can be inactive before
            the proxy disconnects it.
        type: int
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    require_tls:
        aliases:
        - RequireTLS
        description:
        - A Boolean parameter that specifies whether Transport Layer Security (TLS)
            encryption is required for connections to the proxy.
        type: bool
    role_arn:
        aliases:
        - RoleArn
        description:
        - The Amazon Resource Name (ARN) of the IAM role that the proxy uses to access
            secrets in AWS Secrets Manager.
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
        - Tags
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        type: dict
    vpc_security_group_ids:
        aliases:
        - VpcSecurityGroupIds
        description:
        - VPC security group IDs to associate with the new proxy.
        elements: str
        type: list
    vpc_subnet_ids:
        aliases:
        - VpcSubnetIds
        description:
        - VPC subnet IDs to associate with the new proxy.
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

    argument_spec["auth"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "auth_scheme": {
                "type": "str",
                "choices": ["SECRETS"],
                "aliases": ["AuthScheme"],
            },
            "description": {"type": "str", "aliases": ["Description"]},
            "iam_auth": {
                "type": "str",
                "choices": ["DISABLED", "ENABLED", "REQUIRED"],
                "aliases": ["IAMAuth"],
            },
            "secret_arn": {"type": "str", "aliases": ["SecretArn"]},
            "client_password_auth_type": {
                "type": "str",
                "choices": [
                    "MYSQL_NATIVE_PASSWORD",
                    "POSTGRES_MD5",
                    "POSTGRES_SCRAM_SHA_256",
                    "SQL_SERVER_AUTHENTICATION",
                ],
                "aliases": ["ClientPasswordAuthType"],
            },
        },
        "aliases": ["Auth"],
    }
    argument_spec["db_proxy_name"] = {"type": "str", "aliases": ["DBProxyName"]}
    argument_spec["debug_logging"] = {"type": "bool", "aliases": ["DebugLogging"]}
    argument_spec["engine_family"] = {
        "type": "str",
        "choices": ["MYSQL", "POSTGRESQL", "SQLSERVER"],
        "aliases": ["EngineFamily"],
    }
    argument_spec["idle_client_timeout"] = {
        "type": "int",
        "aliases": ["IdleClientTimeout"],
    }
    argument_spec["require_tls"] = {"type": "bool", "aliases": ["RequireTLS"]}
    argument_spec["role_arn"] = {"type": "str", "aliases": ["RoleArn"]}
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags", "resource_tags"]}
    argument_spec["vpc_security_group_ids"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["VpcSecurityGroupIds"],
    }
    argument_spec["vpc_subnet_ids"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["VpcSubnetIds"],
    }
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
            ["role_arn", "engine_family", "db_proxy_name", "auth", "vpc_subnet_ids"],
            True,
        ],
        ["state", "absent", ["db_proxy_name"], True],
        ["state", "get", ["db_proxy_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
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
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/DBProxyName",
        "/properties/EngineFamily",
        "/properties/VpcSubnetIds",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/DBProxyName"]

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
