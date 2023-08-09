#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: eks_cluster
short_description: Create and manages Amazon EKS control planes
description:
- Create and manage Amazon EKS control planes.
options:
    encryption_config:
        aliases:
        - EncryptionConfig
        description:
        - The encryption configuration for the cluster.
        elements: dict
        suboptions:
            provider:
                aliases:
                - Provider
                description:
                - The encryption provider for the cluster.
                suboptions:
                    key_arn:
                        aliases:
                        - KeyArn
                        description:
                        - Amazon Resource Name (ARN) or alias of the KMS key.
                        - The KMS key must be symmetric, created in the same region
                            as the cluster, and if the KMS key was created in a different
                            account, the user must have access to the KMS key.
                        type: str
                type: dict
            resources:
                aliases:
                - Resources
                description:
                - Specifies the resources to be encrypted.
                - The only supported value is secrets.
                elements: str
                type: list
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
    logging:
        aliases:
        - Logging
        description:
        - Enable exporting the Kubernetes control plane logs for your cluster to CloudWatch
            Logs based on log types.
        - By default, cluster control plane logs arent exported to CloudWatch Logs.
        suboptions:
            cluster_logging:
                aliases:
                - ClusterLogging
                description:
                - The cluster control plane logging configuration for your cluster.
                - The cluster control plane logging configuration for your cluster.
                suboptions:
                    enabled_types:
                        aliases:
                        - EnabledTypes
                        description:
                        - Enabled Logging Type.
                        elements: dict
                        suboptions:
                            type:
                                aliases:
                                - Type
                                choices:
                                - api
                                - audit
                                - authenticator
                                - controllerManager
                                - scheduler
                                description:
                                - name of the log type.
                                type: str
                        type: list
                type: dict
        type: dict
    name:
        aliases:
        - Name
        description:
        - The unique name to give to your cluster.
        type: str
    outpost_config:
        aliases:
        - OutpostConfig
        description:
        - An object representing the Outpost configuration to use for AWS EKS outpost
            cluster.
        suboptions:
            control_plane_instance_type:
                aliases:
                - ControlPlaneInstanceType
                description:
                - Specify the Instance type of the machines that should be used to
                    create your cluster.
                type: str
            control_plane_placement:
                aliases:
                - ControlPlanePlacement
                description:
                - Specify the placement group of the control plane machines for your
                    cluster.Specify the placement group of the control plane machines
                    for your cluster.
                suboptions:
                    group_name:
                        aliases:
                        - GroupName
                        description:
                        - Specify the placement group name of the control place machines
                            for your cluster.
                        type: str
                type: dict
            outpost_arns:
                aliases:
                - OutpostArns
                description:
                - Specify one or more Arn(s) of Outpost(s) on which you would like
                    to create your cluster.
                elements: str
                type: list
        type: dict
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    resources_vpc_config:
        aliases:
        - ResourcesVpcConfig
        description:
        - An object representing the VPC configuration to use for an Amazon EKS cluster.
        suboptions:
            endpoint_private_access:
                aliases:
                - EndpointPrivateAccess
                description:
                - Set this value to true to enable private access for your clusters
                    Kubernetes API server endpoint.
                - If you enable private access, Kubernetes API requests from within
                    your clusters VPC use the private VPC endpoint.
                - The default value for this parameter is false, which disables private
                    access for your Kubernetes API server.
                - If you disable private access and you have nodes or AWS Fargate
                    pods in the cluster, then ensure that publicAccessCidrs includes
                    the necessary CIDR blocks for communication with the nodes or
                    Fargate pods.
                type: bool
            endpoint_public_access:
                aliases:
                - EndpointPublicAccess
                description:
                - Set this value to false to disable public access to your clusters
                    Kubernetes API server endpoint.
                - If you disable public access, your clusters Kubernetes API server
                    can only receive requests from within the cluster VPC. The default
                    value for this parameter is true, which enables public access
                    for your Kubernetes API server.
                type: bool
            public_access_cidrs:
                aliases:
                - PublicAccessCidrs
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
                aliases:
                - SecurityGroupIds
                description:
                - Specify one or more security groups for the cross-account elastic
                    network interfaces that Amazon EKS creates to use to allow communication
                    between your worker nodes and the Kubernetes control plane.
                - If you dont specify a security group, the default security group
                    for your VPC is used.
                elements: str
                type: list
            subnet_ids:
                aliases:
                - SubnetIds
                description:
                - Specify subnets for your Amazon EKS nodes.
                - Amazon EKS creates cross-account elastic network interfaces in these
                    subnets to allow communication between your nodes and the Kubernetes
                    control plane.
                elements: str
                type: list
        type: dict
    role_arn:
        aliases:
        - RoleArn
        description:
        - The Amazon Resource Name (ARN) of the IAM role that provides permissions
            for the Kubernetes control plane to make calls to AWS API operations on
            your behalf.
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
        - Tags
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        type: dict
    version:
        aliases:
        - Version
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
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
- amazon.cloud.boto3
"""

EXAMPLES = r"""
- name: Set the cluster name
  set_fact:
    eks_cluster_name: '{{ _resource_prefix }}-cluster'

- name: Create EKS cluster
  amazon.cloud.eks_cluster:
    name: '{{ eks_cluster_name }}'
    resources_vpc_config:
      security_group_ids: "{{ _result_create_security_groups.results | map(attribute='group_id') }}"
      subnet_ids: "{{ _result_create_subnets.results | map(attribute='subnet.id') }}"
      endpoint_public_access: true
      endpoint_private_access: false
      public_access_cidrs:
      - 0.0.0.0/0
    role_arn: '{{ _result_create_iam_role.arn }}'
    tags:
      Name: '{{ _resource_prefix }}-eks-cluster'
    wait_timeout: 900
  register: _result_create_cluster

- name: Describe EKS cluster
  amazon.cloud.eks_cluster:
    name: '{{ eks_cluster_name }}'
    state: describe
  register: _result_get_cluster

- name: List EKS clusters
  amazon.cloud.eks_cluster:
    state: list
  register: _result_list_clusters
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

    argument_spec["encryption_config"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "provider": {
                "type": "dict",
                "options": {"key_arn": {"type": "str", "aliases": ["KeyArn"]}},
                "aliases": ["Provider"],
            },
            "resources": {"type": "list", "elements": "str", "aliases": ["Resources"]},
        },
        "aliases": ["EncryptionConfig"],
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
                                "aliases": ["Type"],
                            }
                        },
                        "aliases": ["EnabledTypes"],
                    }
                },
                "aliases": ["ClusterLogging"],
            }
        },
        "aliases": ["Logging"],
    }
    argument_spec["name"] = {"type": "str", "aliases": ["Name"]}
    argument_spec["resources_vpc_config"] = {
        "type": "dict",
        "options": {
            "endpoint_private_access": {
                "type": "bool",
                "aliases": ["EndpointPrivateAccess"],
            },
            "endpoint_public_access": {
                "type": "bool",
                "aliases": ["EndpointPublicAccess"],
            },
            "public_access_cidrs": {
                "type": "list",
                "elements": "str",
                "aliases": ["PublicAccessCidrs"],
            },
            "security_group_ids": {
                "type": "list",
                "elements": "str",
                "aliases": ["SecurityGroupIds"],
            },
            "subnet_ids": {"type": "list", "elements": "str", "aliases": ["SubnetIds"]},
        },
        "aliases": ["ResourcesVpcConfig"],
    }
    argument_spec["outpost_config"] = {
        "type": "dict",
        "options": {
            "outpost_arns": {
                "type": "list",
                "elements": "str",
                "aliases": ["OutpostArns"],
            },
            "control_plane_instance_type": {
                "type": "str",
                "aliases": ["ControlPlaneInstanceType"],
            },
            "control_plane_placement": {
                "type": "dict",
                "options": {"group_name": {"type": "str", "aliases": ["GroupName"]}},
                "aliases": ["ControlPlanePlacement"],
            },
        },
        "aliases": ["OutpostConfig"],
    }
    argument_spec["role_arn"] = {"type": "str", "aliases": ["RoleArn"]}
    argument_spec["version"] = {"type": "str", "aliases": ["Version"]}
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags", "resource_tags"]}
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
        ["state", "present", ["role_arn", "resources_vpc_config", "name"], True],
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

    type_name = "AWS::EKS::Cluster"

    params = {}

    params["encryption_config"] = module.params.get("encryption_config")
    params["logging"] = module.params.get("logging")
    params["name"] = module.params.get("name")
    params["outpost_config"] = module.params.get("outpost_config")
    params["resources_vpc_config"] = module.params.get("resources_vpc_config")
    params["role_arn"] = module.params.get("role_arn")
    params["tags"] = module.params.get("tags")
    params["version"] = module.params.get("version")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/OutpostConfig",
        "/properties/EncryptionConfig",
        "/properties/KubernetesNetworkConfig",
        "/properties/Name",
        "/properties/RoleArn",
        "/properties/ResourcesVpcConfig/SubnetIds",
        "/properties/ResourcesVpcConfig/SecurityGroupIds",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/Name"]

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
