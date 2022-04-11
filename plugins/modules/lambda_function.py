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
module: lambda_function
short_description: Create and manage Lambda functions
description: Creates and manage Lambda functions (list, create, update, describe,
    delete).
options:
    architectures:
        choices:
        - arm64
        - x86_64
        description:
        - Not Provived.
        elements: str
        type: list
    code:
        description:
        - The code for the function.
        required: true
        suboptions:
            image_uri:
                description:
                - I(image_uri).
                type: str
            s3_bucket:
                description:
                - An Amazon S3 bucket in the same AWS Region as your function.
                - The bucket can be in a different AWS account.
                type: str
            s3_key:
                description:
                - The Amazon S3 key of the deployment package.
                type: str
            s3_object_version:
                description:
                - For versioned objects, the version of the deployment package object
                    to use.
                type: str
            zip_file:
                description:
                - The source code of your Lambda function.
                - If you include your function source inline with this parameter,
                    AWS CloudFormation places it in a file named index and zips it
                    to create a deployment package..
                type: str
        type: dict
    code_signing_config_arn:
        description:
        - A unique Arn for I(code_signing_config) resource
        type: str
    dead_letter_config:
        description:
        - A dead letter queue configuration that specifies the queue or topic where
            Lambda sends asynchronous events when they fail processing.The dead-letter
            queue for failed asynchronous invocations.
        suboptions:
            target_arn:
                description:
                - The Amazon Resource Name (ARN) of an Amazon SQS queue or Amazon
                    SNS topic.
                type: str
        type: dict
    description:
        description:
        - A description of the function.
        type: str
    environment:
        description:
        - Environment variables that are accessible from function code during execution.A
            functions environment variable settings.
        suboptions:
            variables:
                description:
                - Environment variable key-value pairs.
                type: dict
        type: dict
    ephemeral_storage:
        description:
        - A functions ephemeral storage settings.A functions ephemeral storage settings.
        suboptions:
            size:
                description:
                - The amount of ephemeral storage that your function has access to.
                required: true
                type: int
        type: dict
    file_system_configs:
        description:
        - Connection settings for an Amazon EFS file system.
        - To connect a function to a file system, a mount target must be available
            in every Availability Zone that your function connects to.
        - If your template contains an AWS::EFS::I(mount_target) resource, you must
            also specify a I(depends_on) attribute to ensure that the mount target
            is created or updated before the function.
        elements: dict
        suboptions:
            local_mount_path:
                description:
                - The path where the function can access the file system, starting
                    with /mnt/.
                required: true
                type: str
        type: list
    function_name:
        description:
        - The name of the Lambda function, up to 64 characters in length.
        - If you dont specify a name, AWS CloudFormation generates one.
        type: str
    handler:
        description:
        - The name of the method within your code that Lambda calls to execute your
            function.
        - The format includes the file name.
        - It can also include namespaces and other qualifiers, depending on the runtime
        type: str
    image_config:
        description:
        - I(image_config)
        suboptions:
            command:
                description:
                - Command.
                elements: str
                type: list
            entry_point:
                description:
                - I(entry_point).
                elements: str
                type: list
            working_directory:
                description:
                - I(working_directory).
                type: str
        type: dict
    kms_key_arn:
        description:
        - The ARN of the AWS Key Management Service (AWS KMS) key thats used to encrypt
            your functions environment variables.
        - If its not provided, AWS Lambda uses a default service key.
        type: str
    layers:
        description:
        - A list of function layers to add to the functions execution environment.
        - Specify each layer by its ARN, including the version.
        elements: str
        type: list
    memory_size:
        description:
        - The amount of memory that your function has access to.
        - Increasing the functions memory also increases its CPU allocation.
        - The default value is 128 MB. The value must be a multiple of 64 MB.
        type: int
    package_type:
        choices:
        - Image
        - Zip
        description:
        - I(package_type).
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        required: false
        type: bool
    reserved_concurrent_executions:
        description:
        - The number of simultaneous executions to reserve for the function.
        type: int
    role:
        description:
        - The Amazon Resource Name (ARN) of the functions execution role.
        required: true
        type: str
    runtime:
        description:
        - The identifier of the functions runtime.
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
    timeout:
        description:
        - The amount of time that Lambda allows a function to run before stopping
            it.
        - The default is 3 seconds.
        - The maximum allowed value is 900 seconds.
        type: int
    tracing_config:
        description:
        - Set Mode to Active to sample and trace a subset of incoming requests with
            AWS X-Ray.The functions AWS X-Ray tracing configuration.
        - To sample and record incoming requests, set Mode to Active.
        suboptions:
            mode:
                choices:
                - Active
                - PassThrough
                description:
                - The tracing mode.
                type: str
        type: dict
    vpc_config:
        description:
        - For network connectivity to AWS resources in a VPC, specify a list of security
            groups and subnets in the VPC.The VPC security groups and subnets that
            are attached to a Lambda function.
        - When you connect a function to a VPC, Lambda creates an elastic network
            interface for each combination of security group and subnet in the functions
            VPC configuration.
        - The function can only access resources and the internet through that VPC.
        suboptions:
            security_group_ids:
                description:
                - A list of VPC security groups IDs.
                elements: str
                type: list
            subnet_ids:
                description:
                - A list of VPC subnet IDs.
                elements: str
                type: list
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

    argument_spec["code"] = {
        "type": "dict",
        "options": {
            "s3_bucket": {"type": "str"},
            "s3_key": {"type": "str"},
            "s3_object_version": {"type": "str"},
            "zip_file": {"type": "str"},
            "image_uri": {"type": "str"},
        },
        "required": True,
    }
    argument_spec["dead_letter_config"] = {
        "type": "dict",
        "options": {"target_arn": {"type": "str"}},
    }
    argument_spec["description"] = {"type": "str"}
    argument_spec["environment"] = {
        "type": "dict",
        "options": {"variables": {"type": "dict"}},
    }
    argument_spec["ephemeral_storage"] = {
        "type": "dict",
        "options": {"size": {"type": "int", "required": True}},
    }
    argument_spec["file_system_configs"] = {
        "type": "list",
        "elements": "dict",
        "options": {"local_mount_path": {"type": "str", "required": True}},
    }
    argument_spec["function_name"] = {"type": "str"}
    argument_spec["handler"] = {"type": "str"}
    argument_spec["architectures"] = {
        "type": "list",
        "elements": "str",
        "choices": ["arm64", "x86_64"],
    }
    argument_spec["kms_key_arn"] = {"type": "str"}
    argument_spec["layers"] = {"type": "list", "elements": "str"}
    argument_spec["memory_size"] = {"type": "int"}
    argument_spec["reserved_concurrent_executions"] = {"type": "int"}
    argument_spec["role"] = {"type": "str", "required": True}
    argument_spec["runtime"] = {"type": "str"}
    argument_spec["tags"] = {
        "type": "dict",
        "required": False,
        "aliases": ["resource_tags"],
    }
    argument_spec["timeout"] = {"type": "int"}
    argument_spec["tracing_config"] = {
        "type": "dict",
        "options": {"mode": {"type": "str", "choices": ["Active", "PassThrough"]}},
    }
    argument_spec["vpc_config"] = {
        "type": "dict",
        "options": {
            "security_group_ids": {"type": "list", "elements": "str"},
            "subnet_ids": {"type": "list", "elements": "str"},
        },
    }
    argument_spec["code_signing_config_arn"] = {"type": "str"}
    argument_spec["image_config"] = {
        "type": "dict",
        "options": {
            "entry_point": {"type": "list", "elements": "str"},
            "command": {"type": "list", "elements": "str"},
            "working_directory": {"type": "str"},
        },
    }
    argument_spec["package_type"] = {"type": "str", "choices": ["Image", "Zip"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["purge_tags"] = {"type": "bool", "required": False, "default": True}

    required_if = [
        ["state", "present", ["function_name", "role", "code"], True],
        ["state", "absent", ["function_name"], True],
        ["state", "get", ["function_name"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Lambda::Function"

    params = {}

    params["architectures"] = module.params.get("architectures")
    params["code"] = module.params.get("code")
    params["code_signing_config_arn"] = module.params.get("code_signing_config_arn")
    params["dead_letter_config"] = module.params.get("dead_letter_config")
    params["description"] = module.params.get("description")
    params["environment"] = module.params.get("environment")
    params["ephemeral_storage"] = module.params.get("ephemeral_storage")
    params["file_system_configs"] = module.params.get("file_system_configs")
    params["function_name"] = module.params.get("function_name")
    params["handler"] = module.params.get("handler")
    params["image_config"] = module.params.get("image_config")
    params["kms_key_arn"] = module.params.get("kms_key_arn")
    params["layers"] = module.params.get("layers")
    params["memory_size"] = module.params.get("memory_size")
    params["package_type"] = module.params.get("package_type")
    params["reserved_concurrent_executions"] = module.params.get(
        "reserved_concurrent_executions"
    )
    params["role"] = module.params.get("role")
    params["runtime"] = module.params.get("runtime")
    params["tags"] = module.params.get("tags")
    params["timeout"] = module.params.get("timeout")
    params["tracing_config"] = module.params.get("tracing_config")
    params["vpc_config"] = module.params.get("vpc_config")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags", None):
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["function_name"]

    state = module.params.get("state")
    identifier = module.params.get("function_name")

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
