#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: logs_metric_filter
short_description: Specifies a metric filter that describes how CloudWatch Logs extracts
    information from logs and transforms it into Amazon CloudWatch metrics
description:
- Specifies a metric filter that describes how CloudWatch Logs extracts information
    from logs and transforms it into Amazon CloudWatch metrics.
- If you have multiple metric filters that are associated with a log group, all the
    filters are applied to the log streams in that group.
- The maximum number of metric filters that can be associated with a log group is
    100.
options:
    filter_name:
        aliases:
        - FilterName
        description:
        - A name for the metric filter.
        type: str
    filter_pattern:
        aliases:
        - FilterPattern
        description:
        - Pattern that Logs follows to interpret each entry in a log.
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
    identifier:
        description:
        - For compound primary identifiers, to specify the primary identifier as a
            string, list each in the order that they are specified in the identifier
            list definition, separated by '|'.
        - For more details, visit U(https://docs.aws.amazon.com/cloudcontrolapi/latest/userguide/resource-identifier.html).
        type: str
    log_group_name:
        aliases:
        - LogGroupName
        description:
        - Existing log group that you want to associate with this filter.
        type: str
    metric_transformations:
        aliases:
        - MetricTransformations
        description:
        - A collection of information that defines how metric data gets emitted.
        elements: dict
        suboptions:
            default_value:
                aliases:
                - DefaultValue
                description:
                - The value to emit when a filter pattern does not match a log event.
                - This value can be null.
                type: int
            dimensions:
                aliases:
                - Dimensions
                description:
                - the key-value pairs that further define a metric.
                elements: dict
                suboptions:
                    key:
                        aliases:
                        - Key
                        description:
                        - The key of the dimension.
                        - Maximum length of 255.
                        type: str
                    value:
                        aliases:
                        - Value
                        description:
                        - The value of the dimension.
                        - Maximum length of 255.
                        type: str
                type: list
            metric_name:
                aliases:
                - MetricName
                description:
                - The name of the CloudWatch metric.
                - Metric name must be in ASCII format.
                type: str
            metric_namespace:
                aliases:
                - MetricNamespace
                description:
                - The namespace of the CloudWatch metric.
                type: str
            metric_value:
                aliases:
                - MetricValue
                description:
                - The value to publish to the CloudWatch metric when a filter pattern
                    matches a log event.
                type: str
            unit:
                aliases:
                - Unit
                choices:
                - Bits
                - Bits/Second
                - Bytes
                - Bytes/Second
                - Count
                - Count/Second
                - Gigabits
                - Gigabits/Second
                - Gigabytes
                - Gigabytes/Second
                - Kilobits
                - Kilobits/Second
                - Kilobytes
                - Kilobytes/Second
                - Megabits
                - Megabits/Second
                - Megabytes
                - Megabytes/Second
                - Microseconds
                - Milliseconds
                - None
                - Percent
                - Seconds
                - Terabits
                - Terabits/Second
                - Terabytes
                - Terabytes/Second
                description:
                - The unit to assign to the metric.
                - If you omit this, the unit is set as None.
                type: str
        type: list
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

    argument_spec["filter_name"] = {"type": "str", "aliases": ["FilterName"]}
    argument_spec["filter_pattern"] = {"type": "str", "aliases": ["FilterPattern"]}
    argument_spec["log_group_name"] = {"type": "str", "aliases": ["LogGroupName"]}
    argument_spec["metric_transformations"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "default_value": {"type": "int", "aliases": ["DefaultValue"]},
            "metric_name": {"type": "str", "aliases": ["MetricName"]},
            "metric_namespace": {"type": "str", "aliases": ["MetricNamespace"]},
            "metric_value": {"type": "str", "aliases": ["MetricValue"]},
            "unit": {
                "type": "str",
                "choices": [
                    "Bits",
                    "Bits/Second",
                    "Bytes",
                    "Bytes/Second",
                    "Count",
                    "Count/Second",
                    "Gigabits",
                    "Gigabits/Second",
                    "Gigabytes",
                    "Gigabytes/Second",
                    "Kilobits",
                    "Kilobits/Second",
                    "Kilobytes",
                    "Kilobytes/Second",
                    "Megabits",
                    "Megabits/Second",
                    "Megabytes",
                    "Megabytes/Second",
                    "Microseconds",
                    "Milliseconds",
                    "None",
                    "Percent",
                    "Seconds",
                    "Terabits",
                    "Terabits/Second",
                    "Terabytes",
                    "Terabytes/Second",
                ],
                "aliases": ["Unit"],
            },
            "dimensions": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "key": {"type": "str", "aliases": ["Key"]},
                    "value": {"type": "str", "aliases": ["Value"]},
                },
                "aliases": ["Dimensions"],
            },
        },
        "aliases": ["MetricTransformations"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}
    argument_spec["identifier"] = {"type": "str"}

    required_if = [
        ["state", "list", ["log_group_name"], True],
        [
            "state",
            "present",
            [
                "log_group_name",
                "filter_name",
                "metric_transformations",
                "filter_pattern",
                "identifier",
            ],
            True,
        ],
        ["state", "absent", ["log_group_name", "filter_name", "identifier"], True],
        ["state", "get", ["log_group_name", "filter_name", "identifier"], True],
    ]
    mutually_exclusive = [[("log_group_name", "filter_name"), "identifier"]]

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Logs::MetricFilter"

    params = {}

    params["filter_name"] = module.params.get("filter_name")
    params["filter_pattern"] = module.params.get("filter_pattern")
    params["identifier"] = module.params.get("identifier")
    params["log_group_name"] = module.params.get("log_group_name")
    params["metric_transformations"] = module.params.get("metric_transformations")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["/properties/FilterName", "/properties/LogGroupName"]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/LogGroupName", "/properties/FilterName"]
    if (
        state in ("present", "absent", "get", "describe")
        and module.params.get("identifier") is None
    ):
        if not module.params.get("log_group_name") or not module.params.get(
            "filter_name"
        ):
            module.fail_json(
                "You must specify all the ('log_group_name', 'filter_name') identifiers."
            )

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
