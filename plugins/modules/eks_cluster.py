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
module: eks_cluster
short_description: Create and manages Amazon EKS control planes
description: Create and manage Amazon EKS control planes (list, create, update, describe,
    delete).
options:
    encryption_config:
        description:
        - The encryption configuration for the cluster
        elements: dict
        suboptions:
            provider:
                description:
                - The encryption provider for the cluster.
                suboptions:
                    key_arn:
                        description:
                        - Amazon Resource Name (ARN) or alias of the KMS key.
                        - The KMS key must be symmetric, created in the same region
                            as the cluster, and if the KMS key was created in a different
                            account, the user must have access to the KMS key.
                        type: str
                type: dict
            resources:
                description:
                - Specifies the resources to be encrypted.
                - The only supported value is secrets.
                elements: str
                type: list
        type: list
    kubernetes_network_config:
        description:
        - The Kubernetes network configuration for the cluster.
        suboptions:
            ip_family:
                choices:
                - ipv4
                - ipv6
                description:
                - Ipv4 or Ipv6.
                - You can only specify ipv6 for 1.21 and later clusters that use version
                    1.10.1 or later of the Amazon VPC CNI add-on
                type: str
            service_ipv4_cidr:
                description:
                - The CIDR block to assign Kubernetes service IP addresses from.
                - If you dont specify a block, Kubernetes assigns addresses from either
                    the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks.
                - We recommend that you specify a block that does not overlap with
                    resources in other networks that are peered or connected to your
                    VPC.
                type: str
        type: dict
    logging:
        description:
        - Enable exporting the Kubernetes control plane logs for your cluster to CloudWatch
            Logs based on log types.
        - By default, cluster control plane logs arent exported to CloudWatch Logs.
        suboptions:
            cluster_logging:
                description:
                - The cluster control plane logging configuration for your cluster.
                - The cluster control plane logging configuration for your cluster.
                suboptions:
                    enabled_types:
                        description:
                        - Enabled Logging Type
                        elements: dict
                        suboptions:
                            type:
                                choices:
                                - api
                                - audit
                                - authenticator
                                - controllerManager
                                - scheduler
                                description:
                                - name of the log type
                                type: str
                        type: list
                type: dict
        type: dict
    name:
        description:
        - The unique name to give to your cluster.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        required: false
        type: bool
    resources_vpc_config:
        description:
        - An object representing the VPC configuration to use for an Amazon EKS cluster.
        required: true
        suboptions:
            endpoint_private_access:
                description:
                - Set this value to true to enable private access for your clusters
                    Kubernetes API server endpoint.
                - If you enable private access, Kubernetes API requests from within
                    your clusters VPC use the private VPC endpoint.
                - The default value for this parameter is false, which disables private
                    access for your Kubernetes API server.
                - If you disable private access and you have nodes or AWS Fargate
                    pods in the cluster, then ensure that publicI(access_cidrs) includes
                    the necessary CIDR blocks for communication with the nodes or
                    Fargate pods.
                type: bool
            endpoint_public_access:
                description:
                - Set this value to false to disable public access to your clusters
                    Kubernetes API server endpoint.
                - If you disable public access, your clusters Kubernetes API server
                    can only receive requests from within the cluster VPC. The default
                    value for this parameter is true, which enables public access
                    for your Kubernetes API server.
                type: bool
            public_access_cidrs:
                description:
                - The CIDR blocks that are allowed access to your clusters public
                    Kubernetes API server endpoint.
                - Communication to the endpoint from addresses outside of the CIDR
                    blocks that you specify is denied.
                - The default value is 0.0.0.0/0.
                - If youve disabled private endpoint access and you have nodes or
                    AWS Fargate pods in the cluster, then ensure that you specify
                    the necessary CIDR blocks.
                elements: str
                type: list
            security_group_ids:
                description:
                - Specify one or more security groups for the cross-account elastic
                    network interfaces that Amazon EKS creates to use to allow communication
                    between your worker nodes and the Kubernetes control plane.
                - If you dont specify a security group, the default security group
                    for your VPC is used.
                elements: str
                type: list
            subnet_ids:
                description:
                - Specify subnets for your Amazon EKS nodes.
                - Amazon EKS creates cross-account elastic network interfaces in these
                    subnets to allow communication between your nodes and the Kubernetes
                    control plane.
                elements: str
                required: true
                type: list
        type: dict
    role_arn:
        description:
        - The Amazon Resource Name (ARN) of the IAM role that provides permissions
            for the Kubernetes control plane to make calls to AWS API operations on
            your behalf.
        required: true
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
    version:
        description:
        - The desired Kubernetes version for your cluster.
        - If you dont specify a value here, the latest version available in Amazon
            EKS is used.
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
requirements: []
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
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

    argument_spec["encryption_config"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "provider": {"type": "dict", "options": {"key_arn": {"type": "str"}}},
            "resources": {"type": "list", "elements": "str"},
        },
    }
    argument_spec["kubernetes_network_config"] = {
        "type": "dict",
        "options": {
            "service_ipv4_cidr": {"type": "str"},
            "ip_family": {"type": "str", "choices": ["ipv4", "ipv6"]},
        },
    }
    argument_spec["logging"] = {
        "type": "dict",
        "options": {
            "cluster_logging": {
                "type": "dict",
                "options": {
                    "enabled_types": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "type": {
                                "type": "str",
                                "choices": [
                                    "api",
                                    "audit",
                                    "authenticator",
                                    "controllerManager",
                                    "scheduler",
                                ],
                            }
                        },
                    }
                },
            }
        },
    }
    argument_spec["name"] = {"type": "str"}
    argument_spec["resources_vpc_config"] = {
        "type": "dict",
        "options": {
            "endpoint_private_access": {"type": "bool"},
            "endpoint_public_access": {"type": "bool"},
            "public_access_cidrs": {"type": "list", "elements": "str"},
            "security_group_ids": {"type": "list", "elements": "str"},
            "subnet_ids": {"type": "list", "required": True, "elements": "str"},
        },
        "required": True,
    }
    argument_spec["role_arn"] = {"type": "str", "required": True}
    argument_spec["version"] = {"type": "str"}
    argument_spec["tags"] = {
        "type": "dict",
        "required": False,
        "aliases": ["resource_tags"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["purge_tags"] = {"type": "bool", "required": False, "default": True}

    required_if = [
        ["state", "present", ["role_arn", "name", "resources_vpc_config"], True],
        ["state", "absent", ["name"], True],
        ["state", "get", ["name"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::EKS::Cluster"

    params = {}

    params["encryption_config"] = module.params.get("encryption_config")
    params["kubernetes_network_config"] = module.params.get("kubernetes_network_config")
    params["logging"] = module.params.get("logging")
    params["name"] = module.params.get("name")
    params["resources_vpc_config"] = module.params.get("resources_vpc_config")
    params["role_arn"] = module.params.get("role_arn")
    params["tags"] = module.params.get("tags")
    params["version"] = module.params.get("version")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags", None):
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "encryption_config",
        "kubernetes_network_config",
        "name",
        "role_arn",
        "subnet_ids",
        "security_group_ids",
    ]

    state = module.params.get("state")
    identifier = module.params.get("name")

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
