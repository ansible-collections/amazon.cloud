#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: lambda_code_signing_config
short_description: Code signing for AWS Lambda
description:
- Creates and manage code signing for AWS Lambda.
options:
    allowed_publishers:
        aliases:
        - AllowedPublishers
        description:
        - When the CodeSigningConfig is later on attached to a function, the function
            code will be expected to be signed by profiles from this listWhen the
            CodeSigningConfig is later on attached to a function, the function code
            will be expected to be signed by profiles from this list.
        suboptions:
            signing_profile_version_arns:
                aliases:
                - SigningProfileVersionArns
                description:
                - List of Signing profile version Arns.
                elements: str
                type: list
        type: dict
    code_signing_config_arn:
        aliases:
        - CodeSigningConfigArn
        description:
        - A unique Arn for CodeSigningConfig resource.
        type: str
    code_signing_policies:
        aliases:
        - CodeSigningPolicies
        description:
        - Policies to control how to act if a signature is invalidPolicies to control
            how to act if a signature is invalid.
        suboptions:
            untrusted_artifact_on_deployment:
                aliases:
                - UntrustedArtifactOnDeployment
                choices:
                - Enforce
                - Warn
                default: Warn
                description:
                - Indicates how Lambda operations involve updating the code artifact
                    will operate.
                - Default to Warn if not provided.
                type: str
        type: dict
    description:
        aliases:
        - Description
        description:
        - A description of the CodeSigningConfig.
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

    argument_spec["description"] = {"type": "str", "aliases": ["Description"]}
    argument_spec["allowed_publishers"] = {
        "type": "dict",
        "options": {
            "signing_profile_version_arns": {
                "type": "list",
                "elements": "str",
                "aliases": ["SigningProfileVersionArns"],
            }
        },
        "aliases": ["AllowedPublishers"],
    }
    argument_spec["code_signing_policies"] = {
        "type": "dict",
        "options": {
            "untrusted_artifact_on_deployment": {
                "type": "str",
                "default": "Warn",
                "choices": ["Enforce", "Warn"],
                "aliases": ["UntrustedArtifactOnDeployment"],
            }
        },
        "aliases": ["CodeSigningPolicies"],
    }
    argument_spec["code_signing_config_arn"] = {
        "type": "str",
        "aliases": ["CodeSigningConfigArn"],
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
        ["state", "present", ["code_signing_config_arn", "AllowedPublishers"], True],
        ["state", "absent", ["code_signing_config_arn"], True],
        ["state", "get", ["code_signing_config_arn"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Lambda::CodeSigningConfig"

    params = {}

    params["allowed_publishers"] = module.params.get("allowed_publishers")
    params["code_signing_config_arn"] = module.params.get("code_signing_config_arn")
    params["code_signing_policies"] = module.params.get("code_signing_policies")
    params["description"] = module.params.get("description")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = {}

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["CodeSigningConfigArn"]

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
