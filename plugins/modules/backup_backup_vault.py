#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the gouttelette generator tool
# See: https://github.com/ansible-collections/gouttelette


DOCUMENTATION = r"""
module: backup_backup_vault
short_description: Create and manage logical containers where backups are stored
description:
- Creates and manages logical containers where backups are stored.
options:
    access_policy:
        description:
        - Not Provived.
        type: dict
    backup_vault_name:
        description:
        - Not Provived.
        type: str
    backup_vault_tags:
        description:
        - Not Provived.
        type: dict
    encryption_key_arn:
        description:
        - Not Provived.
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
    lock_configuration:
        description:
        - Not Provived.
        suboptions:
            changeable_for_days:
                description:
                - Not Provived.
                type: int
            max_retention_days:
                description:
                - Not Provived.
                type: int
            min_retention_days:
                description:
                - Not Provived.
                type: int
        type: dict
    notifications:
        description:
        - Not Provived.
        suboptions:
            backup_vault_events:
                description:
                - Not Provived.
                elements: str
                type: list
            sns_topic_arn:
                description:
                - Not Provived.
                type: str
        type: dict
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
    AnsibleAWSModule,
)
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

    argument_spec["access_policy"] = {"type": "dict"}
    argument_spec["backup_vault_name"] = {"type": "str"}
    argument_spec["backup_vault_tags"] = {"type": "dict"}
    argument_spec["encryption_key_arn"] = {"type": "str"}
    argument_spec["notifications"] = {
        "type": "dict",
        "options": {
            "backup_vault_events": {"type": "list", "elements": "str"},
            "sns_topic_arn": {"type": "str"},
        },
    }
    argument_spec["lock_configuration"] = {
        "type": "dict",
        "options": {
            "min_retention_days": {"type": "int"},
            "max_retention_days": {"type": "int"},
            "changeable_for_days": {"type": "int"},
        },
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}
    argument_spec["tags"] = {"type": "dict", "aliases": ["resource_tags"]}
    argument_spec["purge_tags"] = {"type": "bool", "default": True}

    required_if = [
        ["state", "present", ["backup_vault_name"], True],
        ["state", "absent", ["backup_vault_name"], True],
        ["state", "get", ["backup_vault_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Backup::BackupVault"

    params = {}

    params["access_policy"] = module.params.get("access_policy")
    params["backup_vault_name"] = module.params.get("backup_vault_name")
    params["backup_vault_tags"] = module.params.get("backup_vault_tags")
    params["encryption_key_arn"] = module.params.get("encryption_key_arn")
    params["lock_configuration"] = module.params.get("lock_configuration")
    params["notifications"] = module.params.get("notifications")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["backup_vault_name", "encryption_key_arn"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["backup_vault_name"]

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
