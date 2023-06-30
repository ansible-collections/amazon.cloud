#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: s3objectlambda_access_point
short_description: Create and manage Object Lambda Access Points used to access S3
    buckets
description:
- Create and manage Object Lambda Access Points used to access S3 buckets.
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
    name:
        aliases:
        - Name
        description:
        - The name you want to assign to this Object lambda Access Point.
        type: str
    object_lambda_configuration:
        aliases:
        - ObjectLambdaConfiguration
        description:
        - The Object lambda Access Point Configuration that configures transformations
            to be applied on the objects on specified S3 ActionsConfiguration to be
            applied to this Object lambda Access Point.
        - It specifies Supporting Access Point, Transformation Configurations.
        - Customers can also set if they like to enable Cloudwatch metrics for accesses
            to this Object lambda Access Point.
        - Default setting for Cloudwatch metrics is disable.
        suboptions:
            allowed_features:
                aliases:
                - AllowedFeatures
                description:
                - Not Provived.
                elements: str
                type: list
            cloud_watch_metrics_enabled:
                aliases:
                - CloudWatchMetricsEnabled
                description:
                - Not Provived.
                type: bool
            supporting_access_point:
                aliases:
                - SupportingAccessPoint
                description:
                - Not Provived.
                type: str
            transformation_configurations:
                aliases:
                - TransformationConfigurations
                description:
                - Configuration to define what content transformation will be applied
                    on which S3 Action.
                elements: dict
                suboptions:
                    actions:
                        aliases:
                        - Actions
                        description:
                        - Not Provived.
                        elements: str
                        type: list
                    content_transformation:
                        aliases:
                        - ContentTransformation
                        description:
                        - Not Provived.
                        suboptions:
                            aws_lambda:
                                aliases:
                                - AwsLambda
                                description:
                                - Not Provived.
                                suboptions:
                                    function_arn:
                                        aliases:
                                        - FunctionArn
                                        description:
                                        - Not Provived.
                                        type: str
                                    function_payload:
                                        aliases:
                                        - FunctionPayload
                                        description:
                                        - Not Provived.
                                        type: str
                                type: dict
                        type: dict
                type: list
        type: dict
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

    argument_spec["name"] = {"type": "str", "aliases": ["Name"]}
    argument_spec["object_lambda_configuration"] = {
        "type": "dict",
        "options": {
            "supporting_access_point": {
                "type": "str",
                "aliases": ["SupportingAccessPoint"],
            },
            "allowed_features": {
                "type": "list",
                "elements": "str",
                "aliases": ["AllowedFeatures"],
            },
            "cloud_watch_metrics_enabled": {
                "type": "bool",
                "aliases": ["CloudWatchMetricsEnabled"],
            },
            "transformation_configurations": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "actions": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["Actions"],
                    },
                    "content_transformation": {
                        "type": "dict",
                        "options": {
                            "aws_lambda": {
                                "type": "dict",
                                "options": {
                                    "function_arn": {
                                        "type": "str",
                                        "aliases": ["FunctionArn"],
                                    },
                                    "function_payload": {
                                        "type": "str",
                                        "aliases": ["FunctionPayload"],
                                    },
                                },
                                "aliases": ["AwsLambda"],
                            }
                        },
                        "aliases": ["ContentTransformation"],
                    },
                },
                "aliases": ["TransformationConfigurations"],
            },
        },
        "aliases": ["ObjectLambdaConfiguration"],
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
        ["state", "present", ["name", "object_lambda_configuration"], True],
        ["state", "absent", ["name"], True],
        ["state", "get", ["name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::S3ObjectLambda::AccessPoint"

    params = {}

    params["name"] = module.params.get("name")
    params["object_lambda_configuration"] = module.params.get(
        "object_lambda_configuration"
    )

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["Name"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["Name"]

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
