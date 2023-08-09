#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: rds_option_group
short_description: Creates and manages an option group
description:
- Creates and manages an option group, to enable and configure features that are specific
    to a particular DB engine.
options:
    engine_name:
        aliases:
        - EngineName
        description:
        - Indicates the name of the engine that this option group can be applied to.
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
    major_engine_version:
        aliases:
        - MajorEngineVersion
        description:
        - Indicates the major engine version associated with this option group.
        type: str
    option_configurations:
        aliases:
        - OptionConfigurations
        description:
        - The I(option_configuration) property type specifies an individual option,
            and its settings, within an AWS::RDS::OptionGroup resource.
        elements: dict
        suboptions:
            db_security_group_memberships:
                aliases:
                - DBSecurityGroupMemberships
                description:
                - A list of DBSecurityGroupMembership name strings used for this option.
                elements: str
                type: list
            option_name:
                aliases:
                - OptionName
                description:
                - The configuration of options to include in a group.
                type: str
            option_settings:
                aliases:
                - OptionSettings
                description:
                - The I(option_setting) property type specifies the value for an option
                    within an I(option_setting) property.
                elements: dict
                suboptions:
                    name:
                        aliases:
                        - Name
                        description:
                        - The name of the option that has settings that you can set.
                        type: str
                    value:
                        aliases:
                        - Value
                        description:
                        - The current value of the option setting.
                        type: str
                type: list
            option_version:
                aliases:
                - OptionVersion
                description:
                - The version for the option.
                type: str
            port:
                aliases:
                - Port
                description:
                - The optional port for the option.
                type: int
            vpc_security_group_memberships:
                aliases:
                - VpcSecurityGroupMemberships
                description:
                - A list of VpcSecurityGroupMembership name strings used for this
                    option.
                elements: str
                type: list
        type: list
    option_group_description:
        aliases:
        - OptionGroupDescription
        description:
        - Provides a description of the option group.
        type: str
    option_group_name:
        aliases:
        - OptionGroupName
        description:
        - Specifies the name of the option group.
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
from ansible_collections.amazon.cloud.plugins.module_utils.core import camel_to_snake


def main():
    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["option_group_name"] = {"type": "str", "aliases": ["OptionGroupName"]}
    argument_spec["option_group_description"] = {
        "type": "str",
        "aliases": ["OptionGroupDescription"],
    }
    argument_spec["engine_name"] = {"type": "str", "aliases": ["EngineName"]}
    argument_spec["major_engine_version"] = {
        "type": "str",
        "aliases": ["MajorEngineVersion"],
    }
    argument_spec["option_configurations"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "db_security_group_memberships": {
                "type": "list",
                "elements": "str",
                "aliases": ["DBSecurityGroupMemberships"],
            },
            "option_name": {"type": "str", "aliases": ["OptionName"]},
            "option_settings": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "name": {"type": "str", "aliases": ["Name"]},
                    "value": {"type": "str", "aliases": ["Value"]},
                },
                "aliases": ["OptionSettings"],
            },
            "option_version": {"type": "str", "aliases": ["OptionVersion"]},
            "port": {"type": "int", "aliases": ["Port"]},
            "vpc_security_group_memberships": {
                "type": "list",
                "elements": "str",
                "aliases": ["VpcSecurityGroupMemberships"],
            },
        },
        "aliases": ["OptionConfigurations"],
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
        [
            "state",
            "present",
            [
                "engine_name",
                "major_engine_version",
                "option_group_name",
                "option_group_description",
            ],
            True,
        ],
        ["state", "absent", ["option_group_name"], True],
        ["state", "get", ["option_group_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::RDS::OptionGroup"

    params = {}

    params["engine_name"] = module.params.get("engine_name")
    params["major_engine_version"] = module.params.get("major_engine_version")
    params["option_configurations"] = module.params.get("option_configurations")
    params["option_group_description"] = module.params.get("option_group_description")
    params["option_group_name"] = module.params.get("option_group_name")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/EngineName",
        "/properties/MajorEngineVersion",
        "/properties/OptionGroupDescription",
        "/properties/OptionGroupName",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/OptionGroupName"]

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
