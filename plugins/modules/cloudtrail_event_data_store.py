#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: cloudtrail_event_data_store
short_description: Creates and manages a new event data store
description:
- Creates and manages a new event data store.
options:
    advanced_event_selectors:
        aliases:
        - AdvancedEventSelectors
        description:
        - Advanced event selectors let you create fine-grained selectors for the following
            AWS CloudTrail event record ?elds.
        - They help you control costs by logging only those events that are important
            to you.
        elements: dict
        suboptions:
            field_selectors:
                aliases:
                - FieldSelectors
                description:
                - A single selector statement in an advanced event selector.
                elements: dict
                suboptions:
                    ends_with:
                        aliases:
                        - EndsWith
                        description:
                        - An operator that includes events that match the last few
                            characters of the event record field specified as the
                            value of Field.
                        elements: str
                        type: list
                    equals:
                        aliases:
                        - Equals
                        description:
                        - An operator that includes events that match the exact value
                            of the event record field specified as the value of Field.
                        - This is the only valid operator that you can use with the
                            readOnly, eventCategory, and resources.type fields.
                        elements: str
                        type: list
                    field:
                        aliases:
                        - Field
                        description:
                        - A field in an event record on which to filter events to
                            be logged.
                        - Supported fields include readOnly, eventCategory, eventSource
                            (for management events), eventName, resources.type, and
                            resources.ARN.
                        type: str
                    not_ends_with:
                        aliases:
                        - NotEndsWith
                        description:
                        - An operator that excludes events that match the last few
                            characters of the event record field specified as the
                            value of Field.
                        elements: str
                        type: list
                    not_equals:
                        aliases:
                        - NotEquals
                        description:
                        - An operator that excludes events that match the exact value
                            of the event record field specified as the value of Field.
                        elements: str
                        type: list
                    not_starts_with:
                        aliases:
                        - NotStartsWith
                        description:
                        - An operator that excludes events that match the first few
                            characters of the event record field specified as the
                            value of Field.
                        elements: str
                        type: list
                    starts_with:
                        aliases:
                        - StartsWith
                        description:
                        - An operator that includes events that match the first few
                            characters of the event record field specified as the
                            value of Field.
                        elements: str
                        type: list
                type: list
            name:
                aliases:
                - Name
                description:
                - An optional, descriptive name for an advanced event selector, such
                    as Log data events for only two S3 buckets.
                type: str
        type: list
    event_data_store_arn:
        aliases:
        - EventDataStoreArn
        description:
        - The ARN of the event data store.
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
    ingestion_enabled:
        aliases:
        - IngestionEnabled
        description:
        - Indicates whether the event data store is ingesting events.
        type: bool
    kms_key_id:
        aliases:
        - KmsKeyId
        description:
        - Specifies the KMS key ID to use to encrypt the events delivered by CloudTrail.
        - The value can be an alias name prefixed by alias/, a fully specified ARN
            to an alias, a fully specified ARN to a key, or a globally unique identifier.
        type: str
    multi_region_enabled:
        aliases:
        - MultiRegionEnabled
        description:
        - Indicates whether the event data store includes events from all regions,
            or only from the region in which it was created.
        type: bool
    name:
        aliases:
        - Name
        description:
        - The name of the event data store.
        type: str
    organization_enabled:
        aliases:
        - OrganizationEnabled
        description:
        - Indicates that an event data store is collecting logged events for an organization.
        type: bool
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    retention_period:
        aliases:
        - RetentionPeriod
        description:
        - The retention period, in days.
        type: int
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
    termination_protection_enabled:
        aliases:
        - TerminationProtectionEnabled
        description:
        - Indicates whether the event data store is protected from termination.
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


def main():
    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["advanced_event_selectors"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "name": {"type": "str", "aliases": ["Name"]},
            "field_selectors": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "field": {"type": "str", "aliases": ["Field"]},
                    "equals": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["Equals"],
                    },
                    "starts_with": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["StartsWith"],
                    },
                    "ends_with": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["EndsWith"],
                    },
                    "not_equals": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["NotEquals"],
                    },
                    "not_starts_with": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["NotStartsWith"],
                    },
                    "not_ends_with": {
                        "type": "list",
                        "elements": "str",
                        "aliases": ["NotEndsWith"],
                    },
                },
                "aliases": ["FieldSelectors"],
            },
        },
        "aliases": ["AdvancedEventSelectors"],
    }
    argument_spec["event_data_store_arn"] = {
        "type": "str",
        "aliases": ["EventDataStoreArn"],
    }
    argument_spec["multi_region_enabled"] = {
        "type": "bool",
        "aliases": ["MultiRegionEnabled"],
    }
    argument_spec["name"] = {"type": "str", "aliases": ["Name"]}
    argument_spec["organization_enabled"] = {
        "type": "bool",
        "aliases": ["OrganizationEnabled"],
    }
    argument_spec["retention_period"] = {"type": "int", "aliases": ["RetentionPeriod"]}
    argument_spec["termination_protection_enabled"] = {
        "type": "bool",
        "aliases": ["TerminationProtectionEnabled"],
    }
    argument_spec["kms_key_id"] = {"type": "str", "aliases": ["KmsKeyId"]}
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags"]}
    argument_spec["ingestion_enabled"] = {
        "type": "bool",
        "aliases": ["IngestionEnabled"],
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
        ["state", "present", ["event_data_store_arn"], True],
        ["state", "absent", ["event_data_store_arn"], True],
        ["state", "get", ["event_data_store_arn"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::CloudTrail::EventDataStore"

    params = {}

    params["advanced_event_selectors"] = module.params.get("advanced_event_selectors")
    params["event_data_store_arn"] = module.params.get("event_data_store_arn")
    params["ingestion_enabled"] = module.params.get("ingestion_enabled")
    params["kms_key_id"] = module.params.get("kms_key_id")
    params["multi_region_enabled"] = module.params.get("multi_region_enabled")
    params["name"] = module.params.get("name")
    params["organization_enabled"] = module.params.get("organization_enabled")
    params["retention_period"] = module.params.get("retention_period")
    params["tags"] = module.params.get("tags")
    params["termination_protection_enabled"] = module.params.get(
        "termination_protection_enabled"
    )

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
    identifier = ["EventDataStoreArn"]

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
