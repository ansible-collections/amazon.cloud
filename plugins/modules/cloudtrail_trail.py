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
module: cloudtrail_trail
short_description: Creates and manages a trail that specifies the settings for delivery
    of log data to an Amazon S3 bucket.
description:
- Creates and manages a trail that specifies the settings for delivery of log data
    to an Amazon S3 bucket.
options:
    cloud_watch_logs_log_group_arn:
        description:
        - Specifies a log group name using an Amazon Resource Name (ARN), a unique
            identifier that represents the log group to which CloudTrail logs will
            be delivered.
        - Not required unless you specify CloudWatchLogsRoleArn.
        type: str
    cloud_watch_logs_role_arn:
        description:
        - Specifies the role for the CloudWatch Logs endpoint to assume to write to
            a users log group.
        type: str
    enable_log_file_validation:
        description:
        - Specifies whether log file validation is enabled.
        - The default is false.
        type: bool
    event_selectors:
        description:
        - The type of email sending events to publish to the event destination.
        elements: dict
        suboptions:
            data_resources:
                description:
                - CloudTrail supports data event logging for Amazon S3 objects and
                    AWS Lambda functions.
                - You can specify up to 250 resources for an individual event selector,
                    but the total number of data resources cannot exceed 250 across
                    all event selectors in a trail.
                - This limit does not apply if you configure resource logging for
                    all data events.
                elements: dict
                suboptions:
                    type:
                        description:
                        - The resource type in which you want to log data events.
                        - You can specify AWS::S3::Object or AWS::Lambda::Function
                            resources.
                        type: str
                    values:
                        description:
                        - An array of Amazon Resource Name (ARN) strings or partial
                            ARN strings for the specified objects.
                        elements: str
                        type: list
                type: list
            exclude_management_event_sources:
                description:
                - An optional list of service event sources from which you do not
                    want management events to be logged on your trail.
                - In this release, the list can be empty (disables the filter), or
                    it can filter out AWS Key Management Service events by containing
                    kms.amazonaws.com.
                - By default, I(exclude_management_event_sources) is empty, and AWS
                    KMS events are included in events that are logged to your trail.
                elements: str
                type: list
            include_management_events:
                description:
                - Specify if you want your event selector to include management events
                    for your trail.
                type: bool
            read_write_type:
                choices:
                - All
                - ReadOnly
                - WriteOnly
                description:
                - Specify if you want your trail to log read-only events, write-only
                    events, or all.
                - For example, the EC2 GetConsoleOutput is a read-only API operation
                    and RunInstances is a write-only API operation.
                type: str
        type: list
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    include_global_service_events:
        description:
        - Specifies whether the trail is publishing events from global services such
            as IAM to the log files.
        type: bool
    insight_selectors:
        description:
        - A string that contains insight types that are logged on a trail.
        elements: dict
        suboptions:
            insight_type:
                description:
                - The type of insight to log on a trail.
                type: str
        type: list
    is_logging:
        description:
        - Whether the CloudTrail is currently logging AWS API calls.
        type: bool
    is_multi_region_trail:
        description:
        - Specifies whether the trail applies only to the current region or to all
            regions.
        - The default is false.
        - If the trail exists only in the current region and this value is set to
            true, shadow trails (replications of the trail) will be created in the
            other regions.
        - If the trail exists in all regions and this value is set to false, the trail
            will remain in the region where it was created, and its shadow trails
            in other regions will be deleted.
        - As a best practice, consider using trails that log events in all regions.
        type: bool
    is_organization_trail:
        description:
        - Specifies whether the trail is created for all accounts in an organization
            in AWS Organizations, or only for the current AWS account.
        - The default is false, and cannot be true unless the call is made on behalf
            of an AWS account that is the master account for an organization in AWS
            Organizations.
        type: bool
    kms_key_id:
        description:
        - Specifies the KMS key ID to use to encrypt the logs delivered by CloudTrail.
        - The value can be an alias name prefixed by alias/, a fully specified ARN
            to an alias, a fully specified ARN to a key, or a globally unique identifier.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    s3_bucket_name:
        description:
        - Specifies the name of the Amazon S3 bucket designated for publishing log
            files.
        - See Amazon S3 Bucket Naming Requirements.
        type: str
    s3_key_prefix:
        description:
        - Specifies the Amazon S3 key prefix that comes after the name of the bucket
            you have designated for log file delivery.
        - For more information, see Finding Your CloudTrail Log Files.
        - The maximum length is 200 characters.
        type: str
    sns_topic_name:
        description:
        - Specifies the name of the Amazon SNS topic defined for notification of log
            file delivery.
        - The maximum length is 256 characters.
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
        type: dict
    trail_name:
        description:
        - Not Provived.
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
requirements: []
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

    argument_spec["cloud_watch_logs_log_group_arn"] = {"type": "str"}
    argument_spec["cloud_watch_logs_role_arn"] = {"type": "str"}
    argument_spec["enable_log_file_validation"] = {"type": "bool"}
    argument_spec["event_selectors"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "data_resources": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "type": {"type": "str"},
                    "values": {"type": "list", "elements": "str"},
                },
            },
            "include_management_events": {"type": "bool"},
            "read_write_type": {
                "type": "str",
                "choices": ["All", "ReadOnly", "WriteOnly"],
            },
            "exclude_management_event_sources": {"type": "list", "elements": "str"},
        },
    }
    argument_spec["include_global_service_events"] = {"type": "bool"}
    argument_spec["is_logging"] = {"type": "bool"}
    argument_spec["is_multi_region_trail"] = {"type": "bool"}
    argument_spec["is_organization_trail"] = {"type": "bool"}
    argument_spec["kms_key_id"] = {"type": "str"}
    argument_spec["s3_bucket_name"] = {"type": "str"}
    argument_spec["s3_key_prefix"] = {"type": "str"}
    argument_spec["sns_topic_name"] = {"type": "str"}
    argument_spec["tags"] = {"type": "dict", "aliases": ["resource_tags"]}
    argument_spec["trail_name"] = {"type": "str"}
    argument_spec["insight_selectors"] = {
        "type": "list",
        "elements": "dict",
        "options": {"insight_type": {"type": "str"}},
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
        ["state", "present", ["s3_bucket_name", "is_logging", "trail_name"], True],
        ["state", "absent", ["trail_name"], True],
        ["state", "get", ["trail_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::CloudTrail::Trail"

    params = {}

    params["cloud_watch_logs_log_group_arn"] = module.params.get(
        "cloud_watch_logs_log_group_arn"
    )
    params["cloud_watch_logs_role_arn"] = module.params.get("cloud_watch_logs_role_arn")
    params["enable_log_file_validation"] = module.params.get(
        "enable_log_file_validation"
    )
    params["event_selectors"] = module.params.get("event_selectors")
    params["include_global_service_events"] = module.params.get(
        "include_global_service_events"
    )
    params["insight_selectors"] = module.params.get("insight_selectors")
    params["is_logging"] = module.params.get("is_logging")
    params["is_multi_region_trail"] = module.params.get("is_multi_region_trail")
    params["is_organization_trail"] = module.params.get("is_organization_trail")
    params["kms_key_id"] = module.params.get("kms_key_id")
    params["s3_bucket_name"] = module.params.get("s3_bucket_name")
    params["s3_key_prefix"] = module.params.get("s3_key_prefix")
    params["sns_topic_name"] = module.params.get("sns_topic_name")
    params["tags"] = module.params.get("tags")
    params["trail_name"] = module.params.get("trail_name")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["trail_name"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["trail_name"]

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
