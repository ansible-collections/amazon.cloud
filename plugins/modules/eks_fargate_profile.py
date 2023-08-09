#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: eks_fargate_profile
short_description: Creates and manage AWS Fargate profiles
description:
- Creates and manage AWS Fargate profiles for your Amazon EKS cluster.
- You must have at least one Fargate profile in a cluster to be able to run pods on
    Fargate.
options:
    cluster_name:
        aliases:
        - ClusterName
        description:
        - Name of the Cluster.
        type: str
    fargate_profile_name:
        aliases:
        - FargateProfileName
        description:
        - Name of FargateProfile.
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
    pod_execution_role_arn:
        aliases:
        - PodExecutionRoleArn
        description:
        - The IAM policy arn for pods.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    selectors:
        aliases:
        - Selectors
        description:
        - Not Provived.
        elements: dict
        suboptions:
            labels:
                aliases:
                - Labels
                description:
                - A key-value pair to associate with a pod.
                elements: dict
                suboptions:
                    key:
                        aliases:
                        - Key
                        description:
                        - The key name of the label.
                        type: str
                    value:
                        aliases:
                        - Value
                        description:
                        - The value for the label.
                        type: str
                type: list
            namespace:
                aliases:
                - Namespace
                description:
                - Not Provived.
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
    subnets:
        aliases:
        - Subnets
        description:
        - Not Provived.
        elements: str
        type: list
    tags:
        aliases:
        - Tags
        - resource_tags
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
version_added: 0.2.0
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
- amazon.cloud.boto3
"""

EXAMPLES = r"""
- name: Set the cluster name
  set_fact:
    eks_cluster_name: '{{ _resource_prefix }}-cluster'

- name: Define EKS facts
  set_fact:
    eks_fargate_profile_name_a: '{{ _resource_prefix }}-fp-a'
    eks_fargate_profile_name_b: '{{ _resource_prefix }}-fp-b'
    eks_subnets:
    - zone: a
      cidr: 10.0.1.0/24
      type: private
      tag: internal-elb
    - zone: b
      cidr: 10.0.2.0/24
      type: public
      tag: elb
    eks_security_groups:
    - name: '{{ eks_cluster_name }}-control-plane-sg'
      description: EKS Control Plane Security Group
      rules:
      - group_name: '{{ eks_cluster_name }}-workers-sg'
        group_desc: EKS Worker Security Group
        ports: 443
        proto: tcp
      rules_egress:
      - group_name: '{{ eks_cluster_name }}-workers-sg'
        group_desc: EKS Worker Security Group
        from_port: 1025
        to_port: 65535
        proto: tcp
    - name: '{{ eks_cluster_name }}-workers-sg'
      description: EKS Worker Security Group
      rules:
      - group_name: '{{ eks_cluster_name }}-workers-sg'
        proto: tcp
        from_port: 1
        to_port: 65535
      - group_name: '{{ eks_cluster_name }}-control-plane-sg'
        ports: 10250
        proto: tcp

- name: Define selector
  set_fact:
    selectors:
    - labels:
      - key: test
        value: test
      namespace: fp-default

- name: Define the tags
  set_fact:
    tags:
      Foo: foo
      bar: Bar

- name: Create Fargate Profile a with wait
  amazon.cloud.eks_fargate_profile:
    fargate_profile_name: '{{ eks_fargate_profile_name_a }}'
    state: present
    cluster_name: '{{ eks_cluster_name }}'
    pod_execution_role_arn: '{{ _result_create_iam_role_fp.arn }}'
    subnets: "{{_result_create_subnets.results|selectattr('subnet.tags.Name', 'contains', 'private') | map(attribute='subnet.id') }}"
    selectors: '{{ selectors }}'
    wait: true
    tags: '{{ tags }}'
  register: _result_create_fp

- name: List Fargate Profiles
  amazon.cloud.eks_fargate_profile:
    state: list
    cluster_name: '{{ eks_cluster_name }}'
  register: _result_list_fp

- name: Update tags in Fargate Profile a with wait (check mode)
  amazon.cloud.eks_fargate_profile:
    fargate_profile_name: '{{ eks_fargate_profile_name_a }}'
    state: present
    cluster_name: '{{ eks_cluster_name }}'
    pod_execution_role_arn: '{{ _result_create_iam_role_fp.arn }}'
    subnets: "{{_result_create_subnets.results|selectattr('subnet.tags.Name', 'contains', 'private') | map(attribute='subnet.id') }}"
    selectors: '{{ selectors }}'
    wait: true
    tags:
      env: test
      test: foo
  check_mode: true
  register: _result_update_tags_fp

- name: Delete Fargate Profile a
  amazon.cloud.eks_fargate_profile:
    fargate_profile_name: '{{ eks_fargate_profile_name_a }}'
    cluster_name: '{{ eks_cluster_name }}'
    state: absent
    wait: true
    wait_timeout: 900
  register: _result_delete_fp
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

    argument_spec["cluster_name"] = {"type": "str", "aliases": ["ClusterName"]}
    argument_spec["fargate_profile_name"] = {
        "type": "str",
        "aliases": ["FargateProfileName"],
    }
    argument_spec["pod_execution_role_arn"] = {
        "type": "str",
        "aliases": ["PodExecutionRoleArn"],
    }
    argument_spec["subnets"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["Subnets"],
    }
    argument_spec["selectors"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "namespace": {"type": "str", "aliases": ["Namespace"]},
            "labels": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "key": {"type": "str", "aliases": ["Key"]},
                    "value": {"type": "str", "aliases": ["Value"]},
                },
                "aliases": ["Labels"],
            },
        },
        "aliases": ["Selectors"],
    }
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
    argument_spec["identifier"] = {"type": "str"}

    required_if = [
        ["state", "list", ["cluster_name"], True],
        [
            "state",
            "present",
            [
                "pod_execution_role_arn",
                "fargate_profile_name",
                "cluster_name",
                "selectors",
                "identifier",
            ],
            True,
        ],
        [
            "state",
            "absent",
            ["cluster_name", "fargate_profile_name", "identifier"],
            True,
        ],
        ["state", "get", ["cluster_name", "fargate_profile_name", "identifier"], True],
    ]
    mutually_exclusive = [[("cluster_name", "fargate_profile_name"), "identifier"]]

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::EKS::FargateProfile"

    params = {}

    params["cluster_name"] = module.params.get("cluster_name")
    params["fargate_profile_name"] = module.params.get("fargate_profile_name")
    params["identifier"] = module.params.get("identifier")
    params["pod_execution_role_arn"] = module.params.get("pod_execution_role_arn")
    params["selectors"] = module.params.get("selectors")
    params["subnets"] = module.params.get("subnets")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/ClusterName",
        "/properties/FargateProfileName",
        "/properties/PodExecutionRoleArn",
        "/properties/Subnets",
        "/properties/Selectors",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "delete", "list", "update"]

    state = module.params.get("state")
    identifier = ["/properties/ClusterName", "/properties/FargateProfileName"]
    if (
        state in ("present", "absent", "get", "describe")
        and module.params.get("identifier") is None
    ):
        if not module.params.get("cluster_name") or not module.params.get(
            "fargate_profile_name"
        ):
            module.fail_json(
                "You must specify all the ('cluster_name', 'fargate_profile_name') identifiers."
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
