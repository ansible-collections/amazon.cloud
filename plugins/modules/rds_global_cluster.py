#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: rds_global_cluster
short_description: Creates and manages an Amazon Aurora global database spread across
    multiple AWS Regions
description:
- Creates and manages an Amazon Aurora global database spread across multiple AWS
    Regions.
options:
    deletion_protection:
        aliases:
        - DeletionProtection
        description:
        - The deletion protection setting for the new global database.
        - The global database cant be deleted when deletion protection is enabled.
        type: bool
    engine:
        aliases:
        - Engine
        choices:
        - aurora
        - aurora-mysql
        - aurora-postgresql
        description:
        - The name of the database engine to be used for this DB cluster.
        - 'Valid Values: aurora (for MySQL 5.6-compatible Aurora), aurora-mysql (for
            MySQL 5.7-compatible Aurora).'
        - If you specify the SourceDBClusterIdentifier property, dont specify this
            property.
        - The value is inherited from the cluster.
        type: str
    engine_version:
        aliases:
        - EngineVersion
        description:
        - The version number of the database engine to use.
        - If you specify the SourceDBClusterIdentifier property, dont specify this
            property.
        - The value is inherited from the cluster.
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
    global_cluster_identifier:
        aliases:
        - GlobalClusterIdentifier
        description:
        - The cluster identifier of the new global database cluster.
        - This parameter is stored as a lowercase string.
        type: str
    source_db_cluster_identifier:
        aliases:
        - SourceDBClusterIdentifier
        description:
        - The Amazon Resource Name (ARN) to use as the primary cluster of the global
            database.
        - This parameter is optional.
        - This parameter is stored as a lowercase string.
        suboptions: {}
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
    storage_encrypted:
        aliases:
        - StorageEncrypted
        description:
        - The storage encryption setting for the new global database cluster.
        - If you specify the SourceDBClusterIdentifier property, dont specify this
            property.
        - The value is inherited from the cluster.
        type: bool
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

    argument_spec["engine"] = {
        "type": "str",
        "choices": ["aurora", "aurora-mysql", "aurora-postgresql"],
        "aliases": ["Engine"],
    }
    argument_spec["engine_version"] = {"type": "str", "aliases": ["EngineVersion"]}
    argument_spec["deletion_protection"] = {
        "type": "bool",
        "aliases": ["DeletionProtection"],
    }
    argument_spec["global_cluster_identifier"] = {
        "type": "str",
        "aliases": ["GlobalClusterIdentifier"],
    }
    argument_spec["source_db_cluster_identifier"] = {
        "type": "str",
        "options": {},
        "aliases": ["SourceDBClusterIdentifier"],
    }
    argument_spec["storage_encrypted"] = {
        "type": "bool",
        "aliases": ["StorageEncrypted"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}

    required_if = [
        ["state", "present", ["global_cluster_identifier"], True],
        ["state", "absent", ["global_cluster_identifier"], True],
        ["state", "get", ["global_cluster_identifier"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::RDS::GlobalCluster"

    params = {}

    params["deletion_protection"] = module.params.get("deletion_protection")
    params["engine"] = module.params.get("engine")
    params["engine_version"] = module.params.get("engine_version")
    params["global_cluster_identifier"] = module.params.get("global_cluster_identifier")
    params["source_db_cluster_identifier"] = module.params.get(
        "source_db_cluster_identifier"
    )
    params["storage_encrypted"] = module.params.get("storage_encrypted")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "GlobalClusterIdentifier",
        "SourceDBClusterIdentifier",
        "StorageEncrypted",
        "Engine",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["GlobalClusterIdentifier"]

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
