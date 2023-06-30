#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: backup_framework
short_description: Create and manage frameworks with one or more controls
description:
- Creates and manages frameworks with one or more controls.
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
    framework_arn:
        aliases:
        - FrameworkArn
        description:
        - An Amazon Resource Name (ARN) that uniquely identifies Framework as a resource.
        type: str
    framework_controls:
        aliases:
        - FrameworkControls
        description:
        - Contains detailed information about all of the controls of a framework.
        - Each framework must contain at least one control.
        elements: dict
        suboptions:
            control_input_parameters:
                aliases:
                - ControlInputParameters
                description:
                - A list of I(parameter_name) and I(parameter_value) pairs.
                elements: dict
                suboptions:
                    parameter_name:
                        aliases:
                        - ParameterName
                        description:
                        - Not Provived.
                        type: str
                    parameter_value:
                        aliases:
                        - ParameterValue
                        description:
                        - Not Provived.
                        type: str
                type: list
            control_name:
                aliases:
                - ControlName
                description:
                - The name of a control.
                - This name is between 1 and 256 characters.
                type: str
            control_scope:
                aliases:
                - ControlScope
                description:
                - The scope of a control.
                - The control scope defines what the control will evaluate.
                - 'Three examples of control scopes are: a specific backup plan, all
                    backup plans with a specific tag, or all backup plans.'
                suboptions:
                    compliance_resource_ids:
                        aliases:
                        - ComplianceResourceIds
                        description:
                        - The ID of the only AWS resource that you want your control
                            scope to contain.
                        elements: str
                        type: list
                    compliance_resource_types:
                        aliases:
                        - ComplianceResourceTypes
                        description:
                        - Describes whether the control scope includes one or more
                            types of resources, such as EFS or RDS.
                        elements: str
                        type: list
                    tags:
                        aliases:
                        - Tags
                        description:
                        - A key-value pair to associate with a resource.
                        elements: dict
                        suboptions:
                            key:
                                aliases:
                                - Key
                                description:
                                - The key name of the tag.
                                - You can specify a value that is 1 to 128 Unicode
                                    characters in length and cannot be prefixed with
                                    aws:.
                                - 'You can use any of the following characters: the
                                    set of Unicode letters, digits, whitespace, _,
                                    ., /, =, +, and -.'
                                type: str
                            value:
                                aliases:
                                - Value
                                description:
                                - The value for the tag.
                                - You can specify a value that is 0 to 256 Unicode
                                    characters in length and cannot be prefixed with
                                    aws:.
                                - 'You can use any of the following characters: the
                                    set of Unicode letters, digits, whitespace, _,
                                    ., /, =, +, and -.'
                                type: str
                        type: list
                type: dict
        type: list
    framework_description:
        aliases:
        - FrameworkDescription
        description:
        - An optional description of the framework with a maximum 1,024 characters.
        type: str
    framework_name:
        aliases:
        - FrameworkName
        description:
        - The unique name of a framework.
        - This name is between 1 and 256 characters, starting with a letter, and consisting
            of letters (a-z, A-Z), numbers (0-9), and underscores (_).
        type: str
    framework_tags:
        aliases:
        - FrameworkTags
        description:
        - A key-value pair to associate with a resource.
        elements: dict
        suboptions:
            key:
                aliases:
                - Key
                description:
                - The key name of the tag.
                - You can specify a value that is 1 to 128 Unicode characters in length
                    and cannot be prefixed with aws:.
                - 'You can use any of the following characters: the set of Unicode
                    letters, digits, whitespace, _, ., /, =, +, and -.'
                type: str
            value:
                aliases:
                - Value
                description:
                - The value for the tag.
                - You can specify a value that is 0 to 256 Unicode characters in length
                    and cannot be prefixed with aws:.
                - 'You can use any of the following characters: the set of Unicode
                    letters, digits, whitespace, _, ., /, =, +, and -.'
                type: str
        type: list
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

    argument_spec["framework_name"] = {"type": "str", "aliases": ["FrameworkName"]}
    argument_spec["framework_description"] = {
        "type": "str",
        "aliases": ["FrameworkDescription"],
    }
    argument_spec["framework_arn"] = {"type": "str", "aliases": ["FrameworkArn"]}
    argument_spec["framework_controls"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "control_name": {"type": "str", "aliases": ["ControlName"]},
            "control_input_parameters": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "parameter_name": {"type": "str", "aliases": ["ParameterName"]},
                    "parameter_value": {"type": "str", "aliases": ["ParameterValue"]},
                },
                "aliases": ["ControlInputParameters"],
            },
            "control_scope": {
                "type": "dict",
                "options": {
                    "compliance_resource_ids": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["ComplianceResourceIds"],
                    },
                    "compliance_resource_types": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["ComplianceResourceTypes"],
                    },
                    "tags": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "key": {"type": "str", "aliases": ["Key"]},
                            "value": {"type": "str", "aliases": ["Value"]},
                        },
                        "aliases": ["Tags"],
                    },
                },
                "aliases": ["ControlScope"],
            },
        },
        "aliases": ["FrameworkControls"],
    }
    argument_spec["framework_tags"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "key": {"type": "str", "aliases": ["Key"]},
            "value": {"type": "str", "aliases": ["Value"]},
        },
        "aliases": ["FrameworkTags"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags"]}
    argument_spec["purge_tags"] = {"type": "bool", "default": True}

    required_if = [
        ["state", "present", ["framework_controls", "framework_arn"], True],
        ["state", "absent", ["framework_arn"], True],
        ["state", "get", ["framework_arn"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Backup::Framework"

    params = {}

    params["framework_arn"] = module.params.get("framework_arn")
    params["framework_controls"] = module.params.get("framework_controls")
    params["framework_description"] = module.params.get("framework_description")
    params["framework_name"] = module.params.get("framework_name")
    params["framework_tags"] = module.params.get("framework_tags")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["FrameworkName"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["FrameworkArn"]

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
