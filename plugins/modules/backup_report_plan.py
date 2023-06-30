#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: backup_report_plan
short_description: Create and manage report plans
description:
- Creates and manages report plans.
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
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    report_delivery_channel:
        aliases:
        - ReportDeliveryChannel
        description:
        - A structure that contains information about where and how to deliver your
            reports, specifically your Amazon S3 bucket name, S3 key prefix, and the
            formats of your reports.
        suboptions:
            formats:
                aliases:
                - Formats
                description:
                - 'A list of the format of your reports: CSV, JSON, or both.'
                - If not specified, the default format is CSV.
                elements: str
                type: list
            s3_bucket_name:
                aliases:
                - S3BucketName
                description:
                - The unique name of the S3 bucket that receives your reports.
                type: str
            s3_key_prefix:
                aliases:
                - S3KeyPrefix
                description:
                - 'The prefix for where AWS Backup Audit Manager delivers your reports
                    to Amazon S3. The prefix is this part of the following path: s3://your-bucket-name/prefix/Backup/us-west-2/year/month/day/report-name.'
                - If not specified, there is no prefix.
                type: str
        type: dict
    report_plan_arn:
        aliases:
        - ReportPlanArn
        description:
        - An Amazon Resource Name (ARN) that uniquely identifies a resource.
        - The format of the ARN depends on the resource type.
        type: str
    report_plan_description:
        aliases:
        - ReportPlanDescription
        description:
        - An optional description of the report plan with a maximum of 1,024 characters.
        type: str
    report_plan_name:
        aliases:
        - ReportPlanName
        description:
        - The unique name of the report plan.
        - The name must be between 1 and 256 characters, starting with a letter, and
            consisting of letters (a-z, A-Z), numbers (0-9), and underscores (_).
        type: str
    report_plan_tags:
        aliases:
        - ReportPlanTags
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
    report_setting:
        aliases:
        - ReportSetting
        description:
        - Identifies the report template for the report.
        - Reports are built using a report template.
        suboptions:
            accounts:
                aliases:
                - Accounts
                description:
                - The list of AWS accounts that a report covers.
                elements: str
                type: list
            framework_arns:
                aliases:
                - FrameworkArns
                description:
                - The Amazon Resource Names (ARNs) of the frameworks a report covers.
                elements: str
                type: list
            organization_units:
                aliases:
                - OrganizationUnits
                description:
                - The list of AWS organization units that a report covers.
                elements: str
                type: list
            regions:
                aliases:
                - Regions
                description:
                - The list of AWS regions that a report covers.
                elements: str
                type: list
            report_template:
                aliases:
                - ReportTemplate
                description:
                - Identifies the report template for the report.
                - Reports are built using a report template.
                - 'The report templates are: C(BACKUP_JOB_REPORT) | C(COPY_JOB_REPORT)
                    | C(RESTORE_JOB_REPORT).'
                type: str
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

    argument_spec["report_plan_name"] = {"type": "str", "aliases": ["ReportPlanName"]}
    argument_spec["report_plan_arn"] = {"type": "str", "aliases": ["ReportPlanArn"]}
    argument_spec["report_plan_description"] = {
        "type": "str",
        "aliases": ["ReportPlanDescription"],
    }
    argument_spec["report_plan_tags"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "key": {"type": "str", "aliases": ["Key"]},
            "value": {"type": "str", "aliases": ["Value"]},
        },
        "aliases": ["ReportPlanTags"],
    }
    argument_spec["report_delivery_channel"] = {
        "type": "dict",
        "options": {
            "formats": {"type": "list", "elements": "str", "aliases": ["Formats"]},
            "s3_bucket_name": {"type": "str", "aliases": ["S3BucketName"]},
            "s3_key_prefix": {"type": "str", "aliases": ["S3KeyPrefix"]},
        },
        "aliases": ["ReportDeliveryChannel"],
    }
    argument_spec["report_setting"] = {
        "type": "dict",
        "options": {
            "report_template": {"type": "str", "aliases": ["ReportTemplate"]},
            "framework_arns": {
                "type": "list",
                "elements": "str",
                "aliases": ["FrameworkArns"],
            },
            "accounts": {"type": "list", "elements": "str", "aliases": ["Accounts"]},
            "organization_units": {
                "type": "list",
                "elements": "str",
                "aliases": ["OrganizationUnits"],
            },
            "regions": {"type": "list", "elements": "str", "aliases": ["Regions"]},
        },
        "aliases": ["ReportSetting"],
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
        [
            "state",
            "present",
            ["report_delivery_channel", "report_setting", "report_plan_arn"],
            True,
        ],
        ["state", "absent", ["report_plan_arn"], True],
        ["state", "get", ["report_plan_arn"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Backup::ReportPlan"

    params = {}

    params["report_delivery_channel"] = module.params.get("report_delivery_channel")
    params["report_plan_arn"] = module.params.get("report_plan_arn")
    params["report_plan_description"] = module.params.get("report_plan_description")
    params["report_plan_name"] = module.params.get("report_plan_name")
    params["report_plan_tags"] = module.params.get("report_plan_tags")
    params["report_setting"] = module.params.get("report_setting")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["ReportPlanName"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["ReportPlanArn"]

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
