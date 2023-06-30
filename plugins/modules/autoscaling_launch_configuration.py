#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: autoscaling_launch_configuration
short_description: Creates and manages a web ACL association.
description:
- Creates and manages a web ACL association.
- Use a web ACL association to define an association between a web ACL and a regional
    application resource, to protect the resource.
options:
    associate_public_ip_address:
        aliases:
        - AssociatePublicIpAddress
        description:
        - For Auto Scaling groups that are running in a virtual private cloud (VPC),
            specifies whether to assign a public IP address to the groups instances.
        type: bool
    block_device_mappings:
        aliases:
        - BlockDeviceMappings
        description:
        - I(block_device_mapping) is a property of AWS::AutoScaling::LaunchConfiguration
            that describes a block device mapping for an Auto Scaling group.
        elements: dict
        suboptions:
            device_name:
                aliases:
                - DeviceName
                description:
                - The device name exposed to the EC2 instance (for example, /dev/sdh
                    or xvdh).
                type: str
            ebs:
                aliases:
                - Ebs
                description:
                - Parameters used to automatically set up EBS volumes when an instance
                    is launched.I(block_device) is a subproperty of I(block_device_mapping)
                    that describes an Amazon EBS volume.
                suboptions:
                    delete_on_termination:
                        aliases:
                        - DeleteOnTermination
                        description:
                        - Indicates whether the volume is deleted on instance termination.
                        type: bool
                    encrypted:
                        aliases:
                        - Encrypted
                        description:
                        - Specifies whether the volume should be encrypted.
                        type: bool
                    iops:
                        aliases:
                        - Iops
                        description:
                        - The number of input/output (I/O) operations per second (IOPS)
                            to provision for the volume.
                        type: int
                    snapshot_id:
                        aliases:
                        - SnapshotId
                        description:
                        - The snapshot ID of the volume to use.
                        type: str
                    throughput:
                        aliases:
                        - Throughput
                        description:
                        - The throughput (MiBps) to provision for a gp3 volume.
                        type: int
                    volume_size:
                        aliases:
                        - VolumeSize
                        description:
                        - The volume size, in GiBs.
                        type: int
                    volume_type:
                        aliases:
                        - VolumeType
                        description:
                        - The volume type.
                        type: str
                type: dict
            no_device:
                aliases:
                - NoDevice
                description:
                - Setting this value to true suppresses the specified device included
                    in the block device mapping of the AMI.
                type: bool
            virtual_name:
                aliases:
                - VirtualName
                description:
                - The name of the virtual device.
                type: str
        type: list
    classic_link_vpc_id:
        aliases:
        - ClassicLinkVPCId
        description:
        - The ID of a ClassicLink-enabled VPC to link your EC2-Classic instances to.
        type: str
    classic_link_vpc_security_groups:
        aliases:
        - ClassicLinkVPCSecurityGroups
        description:
        - The IDs of one or more security groups for the VPC that you specified in
            the ClassicLinkVPCId property.
        elements: str
        type: list
    ebs_optimized:
        aliases:
        - EbsOptimized
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
        aliases:
        - IamInstanceProfile
        description:
        - Provides the name or the Amazon Resource Name (ARN) of the instance profile
            associated with the IAM role for the instance.
        - The instance profile contains the IAM role.
        type: str
    image_id:
        aliases:
        - ImageId
        description:
        - Provides the unique ID of the Amazon Machine Image (AMI) that was assigned
            during registration.
        type: str
    instance_id:
        aliases:
        - InstanceId
        description:
        - The ID of the Amazon EC2 instance you want to use to create the launch configuration.
        type: str
    instance_monitoring:
        aliases:
        - InstanceMonitoring
        description:
        - Controls whether instances in this group are launched with detailed (true)
            or basic (false) monitoring.
        type: bool
    instance_type:
        aliases:
        - InstanceType
        description:
        - Specifies the instance type of the EC2 instance.
        type: str
    kernel_id:
        aliases:
        - KernelId
        description:
        - Provides the ID of the kernel associated with the EC2 AMI.
        type: str
    key_name:
        aliases:
        - KeyName
        description:
        - Provides the name of the EC2 key pair.
        type: str
    launch_configuration_name:
        aliases:
        - LaunchConfigurationName
        description:
        - The name of the launch configuration.
        - This name must be unique per Region per account.
        type: str
    metadata_options:
        aliases:
        - MetadataOptions
        description:
        - The metadata options for the instances.I(metadata_options) is a property
            of AWS::AutoScaling::LaunchConfiguration that describes metadata options
            for the instances.
        suboptions:
            http_endpoint:
                aliases:
                - HttpEndpoint
                description:
                - This parameter enables or disables the HTTP metadata endpoint on
                    your instances.
                type: str
            http_put_response_hop_limit:
                aliases:
                - HttpPutResponseHopLimit
                description:
                - The desired HTTP PUT response hop limit for instance metadata requests.
                type: int
            http_tokens:
                aliases:
                - HttpTokens
                description:
                - The state of token usage for your instance metadata requests.
                type: str
        type: dict
    placement_tenancy:
        aliases:
        - PlacementTenancy
        description:
        - The tenancy of the instance, either default or dedicated.
        type: str
    ram_disk_id:
        aliases:
        - RamDiskId
        description:
        - The ID of the RAM disk to select.
        type: str
    security_groups:
        aliases:
        - SecurityGroups
        description:
        - A list that contains the security groups to assign to the instances in the
            Auto Scaling group.
        elements: str
        type: list
    spot_price:
        aliases:
        - SpotPrice
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
        aliases:
        - UserData
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

    argument_spec["associate_public_ip_address"] = {
        "type": "bool",
        "aliases": ["AssociatePublicIpAddress"],
    }
    argument_spec["block_device_mappings"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "no_device": {"type": "bool", "aliases": ["NoDevice"]},
            "virtual_name": {"type": "str", "aliases": ["VirtualName"]},
            "ebs": {
                "type": "dict",
                "options": {
                    "snapshot_id": {"type": "str", "aliases": ["SnapshotId"]},
                    "volume_type": {"type": "str", "aliases": ["VolumeType"]},
                    "encrypted": {"type": "bool", "aliases": ["Encrypted"]},
                    "iops": {"type": "int", "aliases": ["Iops"]},
                    "volume_size": {"type": "int", "aliases": ["VolumeSize"]},
                    "delete_on_termination": {
                        "type": "bool",
                        "aliases": ["DeleteOnTermination"],
                    },
                    "throughput": {"type": "int", "aliases": ["Throughput"]},
                },
                "aliases": ["Ebs"],
            },
            "device_name": {"type": "str", "aliases": ["DeviceName"]},
        },
        "aliases": ["BlockDeviceMappings"],
    }
    argument_spec["classic_link_vpc_id"] = {
        "type": "str",
        "aliases": ["ClassicLinkVPCId"],
    }
    argument_spec["classic_link_vpc_security_groups"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["ClassicLinkVPCSecurityGroups"],
    }
    argument_spec["ebs_optimized"] = {"type": "bool", "aliases": ["EbsOptimized"]}
    argument_spec["iam_instance_profile"] = {
        "type": "str",
        "aliases": ["IamInstanceProfile"],
    }
    argument_spec["image_id"] = {"type": "str", "aliases": ["ImageId"]}
    argument_spec["instance_id"] = {"type": "str", "aliases": ["InstanceId"]}
    argument_spec["instance_monitoring"] = {
        "type": "bool",
        "aliases": ["InstanceMonitoring"],
    }
    argument_spec["instance_type"] = {"type": "str", "aliases": ["InstanceType"]}
    argument_spec["kernel_id"] = {"type": "str", "aliases": ["KernelId"]}
    argument_spec["key_name"] = {"type": "str", "aliases": ["KeyName"]}
    argument_spec["launch_configuration_name"] = {
        "type": "str",
        "aliases": ["LaunchConfigurationName"],
    }
    argument_spec["metadata_options"] = {
        "type": "dict",
        "options": {
            "http_put_response_hop_limit": {
                "type": "int",
                "aliases": ["HttpPutResponseHopLimit"],
            },
            "http_tokens": {"type": "str", "aliases": ["HttpTokens"]},
            "http_endpoint": {"type": "str", "aliases": ["HttpEndpoint"]},
        },
        "aliases": ["MetadataOptions"],
    }
    argument_spec["placement_tenancy"] = {
        "type": "str",
        "aliases": ["PlacementTenancy"],
    }
    argument_spec["ram_disk_id"] = {"type": "str", "aliases": ["RamDiskId"]}
    argument_spec["security_groups"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["SecurityGroups"],
    }
    argument_spec["spot_price"] = {"type": "str", "aliases": ["SpotPrice"]}
    argument_spec["user_data"] = {"type": "str", "aliases": ["UserData"]}
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
            ["image_id", "launch_configuration_name", "instance_type"],
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
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "AssociatePublicIpAddress",
        "BlockDeviceMappings",
        "ClassicLinkVPCId",
        "ClassicLinkVPCSecurityGroups",
        "EbsOptimized",
        "IamInstanceProfile",
        "ImageId",
        "InstanceId",
        "InstanceMonitoring",
        "InstanceType",
        "KernelId",
        "KeyName",
        "LaunchConfigurationName",
        "MetadataOptions",
        "PlacementTenancy",
        "RamDiskId",
        "SecurityGroups",
        "SpotPrice",
        "UserData",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "delete", "list"]

    state = module.params.get("state")
    identifier = ["LaunchConfigurationName"]

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
