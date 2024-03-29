#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the gouttelette generator tool
# See: https://github.com/ansible-collections/gouttelette


DOCUMENTATION = r"""
module: autoscaling_launch_configuration
short_description: Creates and manages a web ACL association.
description:
- Creates and manages a web ACL association.
- Use a web ACL association to define an association between a web ACL and a regional
    application resource, to protect the resource.
options:
    associate_public_ip_address:
        description:
        - For Auto Scaling groups that are running in a virtual private cloud (VPC),
            specifies whether to assign a public IP address to the groups instances.
        type: bool
    block_device_mappings:
        description:
        - I(block_device_mapping) is a property of AWS::AutoScaling::LaunchConfiguration
            that describes a block device mapping for an Auto Scaling group.
        elements: dict
        suboptions:
            device_name:
                description:
                - The device name exposed to the EC2 instance (for example, /dev/sdh
                    or xvdh).
                type: str
            ebs:
                description:
                - Parameters used to automatically set up EBS volumes when an instance
                    is launched.I(block_device) is a subproperty of I(block_device_mapping)
                    that describes an Amazon EBS volume.
                suboptions:
                    delete_on_termination:
                        description:
                        - Indicates whether the volume is deleted on instance termination.
                        type: bool
                    encrypted:
                        description:
                        - Specifies whether the volume should be encrypted.
                        type: bool
                    iops:
                        description:
                        - The number of input/output (I/O) operations per second (IOPS)
                            to provision for the volume.
                        type: int
                    snapshot_id:
                        description:
                        - The snapshot ID of the volume to use.
                        type: str
                    throughput:
                        description:
                        - The throughput (MiBps) to provision for a gp3 volume.
                        type: int
                    volume_size:
                        description:
                        - The volume size, in GiBs.
                        type: int
                    volume_type:
                        description:
                        - The volume type.
                        type: str
                type: dict
            no_device:
                description:
                - Setting this value to true suppresses the specified device included
                    in the block device mapping of the AMI.
                type: bool
            virtual_name:
                description:
                - The name of the virtual device.
                type: str
        type: list
    classic_link_vpc_id:
        description:
        - The ID of a ClassicLink-enabled VPC to link your EC2-Classic instances to.
        type: str
    classic_link_vpc_security_groups:
        description:
        - The IDs of one or more security groups for the VPC that you specified in
            the ClassicLinkVPCId property.
        elements: str
        type: list
    ebs_optimized:
        description:
        - Specifies whether the launch configuration is optimized for EBS I/O (true)
            or not (false).
        type: bool
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    iam_instance_profile:
        description:
        - Provides the name or the Amazon Resource Name (ARN) of the instance profile
            associated with the IAM role for the instance.
        - The instance profile contains the IAM role.
        type: str
    image_id:
        description:
        - Provides the unique ID of the Amazon Machine Image (AMI) that was assigned
            during registration.
        type: str
    instance_id:
        description:
        - The ID of the Amazon EC2 instance you want to use to create the launch configuration.
        type: str
    instance_monitoring:
        description:
        - Controls whether instances in this group are launched with detailed (true)
            or basic (false) monitoring.
        type: bool
    instance_type:
        description:
        - Specifies the instance type of the EC2 instance.
        type: str
    kernel_id:
        description:
        - Provides the ID of the kernel associated with the EC2 AMI.
        type: str
    key_name:
        description:
        - Provides the name of the EC2 key pair.
        type: str
    launch_configuration_name:
        description:
        - The name of the launch configuration.
        - This name must be unique per Region per account.
        type: str
    metadata_options:
        description:
        - The metadata options for the instances.I(metadata_options) is a property
            of AWS::AutoScaling::LaunchConfiguration that describes metadata options
            for the instances.
        suboptions:
            http_endpoint:
                description:
                - This parameter enables or disables the HTTP metadata endpoint on
                    your instances.
                type: str
            http_put_response_hop_limit:
                description:
                - The desired HTTP PUT response hop limit for instance metadata requests.
                type: int
            http_tokens:
                description:
                - The state of token usage for your instance metadata requests.
                type: str
        type: dict
    placement_tenancy:
        description:
        - The tenancy of the instance, either default or dedicated.
        type: str
    ram_disk_id:
        description:
        - The ID of the RAM disk to select.
        type: str
    security_groups:
        description:
        - A list that contains the security groups to assign to the instances in the
            Auto Scaling group.
        elements: str
        type: list
    spot_price:
        description:
        - The maximum hourly price you are willing to pay for any Spot Instances launched
            to fulfill the request.
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
    user_data:
        description:
        - The Base64-encoded user data to make available to the launched EC2 instances.
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

    argument_spec["associate_public_ip_address"] = {"type": "bool"}
    argument_spec["block_device_mappings"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "no_device": {"type": "bool"},
            "virtual_name": {"type": "str"},
            "ebs": {
                "type": "dict",
                "options": {
                    "snapshot_id": {"type": "str"},
                    "volume_type": {"type": "str"},
                    "encrypted": {"type": "bool"},
                    "iops": {"type": "int"},
                    "volume_size": {"type": "int"},
                    "delete_on_termination": {"type": "bool"},
                    "throughput": {"type": "int"},
                },
            },
            "device_name": {"type": "str"},
        },
    }
    argument_spec["classic_link_vpc_id"] = {"type": "str"}
    argument_spec["classic_link_vpc_security_groups"] = {
        "type": "list",
        "elements": "str",
    }
    argument_spec["ebs_optimized"] = {"type": "bool"}
    argument_spec["iam_instance_profile"] = {"type": "str"}
    argument_spec["image_id"] = {"type": "str"}
    argument_spec["instance_id"] = {"type": "str"}
    argument_spec["instance_monitoring"] = {"type": "bool"}
    argument_spec["instance_type"] = {"type": "str"}
    argument_spec["kernel_id"] = {"type": "str"}
    argument_spec["key_name"] = {"type": "str"}
    argument_spec["launch_configuration_name"] = {"type": "str"}
    argument_spec["metadata_options"] = {
        "type": "dict",
        "options": {
            "http_put_response_hop_limit": {"type": "int"},
            "http_tokens": {"type": "str"},
            "http_endpoint": {"type": "str"},
        },
    }
    argument_spec["placement_tenancy"] = {"type": "str"}
    argument_spec["ram_disk_id"] = {"type": "str"}
    argument_spec["security_groups"] = {"type": "list", "elements": "str"}
    argument_spec["spot_price"] = {"type": "str"}
    argument_spec["user_data"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}

    required_if = [
        [
            "state",
            "present",
            ["instance_type", "launch_configuration_name", "image_id"],
            True,
        ],
        ["state", "absent", ["launch_configuration_name"], True],
        ["state", "get", ["launch_configuration_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::AutoScaling::LaunchConfiguration"

    params = {}

    params["associate_public_ip_address"] = module.params.get(
        "associate_public_ip_address"
    )
    params["block_device_mappings"] = module.params.get("block_device_mappings")
    params["classic_link_vpc_id"] = module.params.get("classic_link_vpc_id")
    params["classic_link_vpc_security_groups"] = module.params.get(
        "classic_link_vpc_security_groups"
    )
    params["ebs_optimized"] = module.params.get("ebs_optimized")
    params["iam_instance_profile"] = module.params.get("iam_instance_profile")
    params["image_id"] = module.params.get("image_id")
    params["instance_id"] = module.params.get("instance_id")
    params["instance_monitoring"] = module.params.get("instance_monitoring")
    params["instance_type"] = module.params.get("instance_type")
    params["kernel_id"] = module.params.get("kernel_id")
    params["key_name"] = module.params.get("key_name")
    params["launch_configuration_name"] = module.params.get("launch_configuration_name")
    params["metadata_options"] = module.params.get("metadata_options")
    params["placement_tenancy"] = module.params.get("placement_tenancy")
    params["ram_disk_id"] = module.params.get("ram_disk_id")
    params["security_groups"] = module.params.get("security_groups")
    params["spot_price"] = module.params.get("spot_price")
    params["user_data"] = module.params.get("user_data")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "associate_public_ip_address",
        "block_device_mappings",
        "classic_link_vpc_id",
        "classic_link_vpc_security_groups",
        "ebs_optimized",
        "iam_instance_profile",
        "image_id",
        "instance_id",
        "instance_monitoring",
        "instance_type",
        "kernel_id",
        "key_name",
        "launch_configuration_name",
        "metadata_options",
        "placement_tenancy",
        "ram_disk_id",
        "security_groups",
        "spot_price",
        "user_data",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "delete", "list"]

    state = module.params.get("state")
    identifier = ["launch_configuration_name"]

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
