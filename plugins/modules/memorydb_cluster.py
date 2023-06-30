#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: memorydb_cluster
short_description: Creates and manages a MemoryDB cluster
description:
- Creates or manages a MemoryDB for Redis cluster. For more information, see U(https://docs.aws.amazon.com/cli/latest/reference/memorydb/create-cluster.html)
options:
    acl_name:
        aliases:
        - ACLName
        description:
        - The name of the Access Control List to associate with the cluster.
        type: str
    auto_minor_version_upgrade:
        aliases:
        - AutoMinorVersionUpgrade
        description:
        - A flag that enables automatic minor version upgrade when set to true.
        - You cannot modify the value of AutoMinorVersionUpgrade after the cluster
            is created.
        - To enable AutoMinorVersionUpgrade on a cluster you must set AutoMinorVersionUpgrade
            to true when you create a cluster.
        type: bool
    cluster_endpoint:
        aliases:
        - ClusterEndpoint
        description:
        - The cluster endpoint.
        suboptions: {}
        type: dict
    cluster_name:
        aliases:
        - ClusterName
        description:
        - The name of the cluster.
        - This value must be unique as it also serves as the cluster identifier.
        type: str
    data_tiering:
        aliases:
        - DataTiering
        choices:
        - 'false'
        - 'true'
        description:
        - Enables data tiering.
        - Data tiering is only supported for clusters using the r6gd node type.
        - This parameter must be set when using r6gd nodes.
        type: str
    description:
        aliases:
        - Description
        description:
        - An optional description of the cluster.
        type: str
    engine_version:
        aliases:
        - EngineVersion
        description:
        - The Redis engine version used by the cluster.
        type: str
    final_snapshot_name:
        aliases:
        - FinalSnapshotName
        description:
        - The user-supplied name of a final cluster snapshot.
        - This is the unique name that identifies the snapshot.
        - MemoryDB creates the snapshot, and then deletes the cluster immediately
            afterward.
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
    kms_key_id:
        aliases:
        - KmsKeyId
        description:
        - The ID of the KMS key used to encrypt the cluster.
        type: str
    maintenance_window:
        aliases:
        - MaintenanceWindow
        description:
        - Specifies the weekly time range during which maintenance on the cluster
            is performed.
        - It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock
            UTC). The minimum maintenance window is a 60 minute period.
        type: str
    node_type:
        aliases:
        - NodeType
        description:
        - The compute and memory capacity of the nodes in the cluster.
        type: str
    num_replicas_per_shard:
        aliases:
        - NumReplicasPerShard
        description:
        - The number of replicas to apply to each shard.
        - The limit is 5.
        type: int
    num_shards:
        aliases:
        - NumShards
        description:
        - The number of shards the cluster will contain.
        type: int
    parameter_group_name:
        aliases:
        - ParameterGroupName
        description:
        - The name of the parameter group associated with the cluster.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    security_group_ids:
        aliases:
        - SecurityGroupIds
        description:
        - One or more Amazon VPC security groups associated with this cluster.
        elements: str
        type: list
    snapshot_arns:
        aliases:
        - SnapshotArns
        description:
        - A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot
            files stored in Amazon S3. The snapshot files are used to populate the
            new cluster.
        - The Amazon S3 object name in the ARN cannot contain any commas.
        elements: str
        type: list
    snapshot_name:
        aliases:
        - SnapshotName
        description:
        - The name of a snapshot from which to restore data into the new cluster.
        - The snapshot status changes to restoring while the new cluster is being
            created.
        type: str
    snapshot_retention_limit:
        aliases:
        - SnapshotRetentionLimit
        description:
        - The number of days for which MemoryDB retains automatic snapshots before
            deleting them.
        - For example, if you set SnapshotRetentionLimit to 5, a snapshot that was
            taken today is retained for 5 days before being deleted.
        type: int
    snapshot_window:
        aliases:
        - SnapshotWindow
        description:
        - The daily time range (in UTC) during which MemoryDB begins taking a daily
            snapshot of your cluster.
        type: str
    sns_topic_arn:
        aliases:
        - SnsTopicArn
        description:
        - The Amazon Resource Name (ARN) of the Amazon Simple Notification Service
            (SNS) topic to which notifications are sent.
        type: str
    sns_topic_status:
        aliases:
        - SnsTopicStatus
        description:
        - The status of the Amazon SNS notification topic.
        - Notifications are sent only if the status is enabled.
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
    subnet_group_name:
        aliases:
        - SubnetGroupName
        description:
        - The name of the subnet group to be used for the cluster.
        type: str
    tags:
        aliases:
        - Tags
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        type: dict
    tls_enabled:
        aliases:
        - TLSEnabled
        description:
        - A flag that enables in-transit encryption when set to true.
        - You cannot modify the value of TransitEncryptionEnabled after the cluster
            is created.
        - To enable in-transit encryption on a cluster you must set TransitEncryptionEnabled
            to true when you create a cluster.
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
version_added: 0.3.0
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
- amazon.cloud.boto3
"""

EXAMPLES = r"""
    - name: Create memorydb cluster with name test-cluster
      amazon.cloud.memorydb_cluster:
        cluster_name: test-cluster
        node_type: db.t4g.small
        acl_name: test-acl
        parameter_group_name: test-parameter-group
        subnet_group_name: test-subnet-group
        wait: True
        wait_timeout: 500
        tags:
          env: "test"

    - name: Describe the cluster
      amazon.cloud.memorydb_cluster:
        cluster_name: test-cluster
        state: describe

    - name: Delete memorydb cluster
      amazon.cloud.memorydb_cluster:
        cluster_name: test-cluster
        state: absent
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
    argument_spec["description"] = {"type": "str", "aliases": ["Description"]}
    argument_spec["node_type"] = {"type": "str", "aliases": ["NodeType"]}
    argument_spec["num_shards"] = {"type": "int", "aliases": ["NumShards"]}
    argument_spec["num_replicas_per_shard"] = {
        "type": "int",
        "aliases": ["NumReplicasPerShard"],
    }
    argument_spec["subnet_group_name"] = {"type": "str", "aliases": ["SubnetGroupName"]}
    argument_spec["security_group_ids"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["SecurityGroupIds"],
    }
    argument_spec["maintenance_window"] = {
        "type": "str",
        "aliases": ["MaintenanceWindow"],
    }
    argument_spec["parameter_group_name"] = {
        "type": "str",
        "aliases": ["ParameterGroupName"],
    }
    argument_spec["snapshot_retention_limit"] = {
        "type": "int",
        "aliases": ["SnapshotRetentionLimit"],
    }
    argument_spec["snapshot_window"] = {"type": "str", "aliases": ["SnapshotWindow"]}
    argument_spec["acl_name"] = {"type": "str", "aliases": ["ACLName"]}
    argument_spec["sns_topic_arn"] = {"type": "str", "aliases": ["SnsTopicArn"]}
    argument_spec["sns_topic_status"] = {"type": "str", "aliases": ["SnsTopicStatus"]}
    argument_spec["tls_enabled"] = {"type": "bool", "aliases": ["TLSEnabled"]}
    argument_spec["data_tiering"] = {
        "type": "str",
        "choices": ["false", "true"],
        "aliases": ["DataTiering"],
    }
    argument_spec["kms_key_id"] = {"type": "str", "aliases": ["KmsKeyId"]}
    argument_spec["snapshot_arns"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["SnapshotArns"],
    }
    argument_spec["snapshot_name"] = {"type": "str", "aliases": ["SnapshotName"]}
    argument_spec["final_snapshot_name"] = {
        "type": "str",
        "aliases": ["FinalSnapshotName"],
    }
    argument_spec["engine_version"] = {"type": "str", "aliases": ["EngineVersion"]}
    argument_spec["cluster_endpoint"] = {
        "type": "dict",
        "options": {},
        "aliases": ["ClusterEndpoint"],
    }
    argument_spec["auto_minor_version_upgrade"] = {
        "type": "bool",
        "aliases": ["AutoMinorVersionUpgrade"],
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

    required_if = [
        ["state", "present", ["acl_name", "cluster_name", "node_type"], True],
        ["state", "absent", ["cluster_name"], True],
        ["state", "get", ["cluster_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::MemoryDB::Cluster"

    params = {}

    params["acl_name"] = module.params.get("acl_name")
    params["auto_minor_version_upgrade"] = module.params.get(
        "auto_minor_version_upgrade"
    )
    params["cluster_endpoint"] = module.params.get("cluster_endpoint")
    params["cluster_name"] = module.params.get("cluster_name")
    params["data_tiering"] = module.params.get("data_tiering")
    params["description"] = module.params.get("description")
    params["engine_version"] = module.params.get("engine_version")
    params["final_snapshot_name"] = module.params.get("final_snapshot_name")
    params["kms_key_id"] = module.params.get("kms_key_id")
    params["maintenance_window"] = module.params.get("maintenance_window")
    params["node_type"] = module.params.get("node_type")
    params["num_replicas_per_shard"] = module.params.get("num_replicas_per_shard")
    params["num_shards"] = module.params.get("num_shards")
    params["parameter_group_name"] = module.params.get("parameter_group_name")
    params["security_group_ids"] = module.params.get("security_group_ids")
    params["snapshot_arns"] = module.params.get("snapshot_arns")
    params["snapshot_name"] = module.params.get("snapshot_name")
    params["snapshot_retention_limit"] = module.params.get("snapshot_retention_limit")
    params["snapshot_window"] = module.params.get("snapshot_window")
    params["sns_topic_arn"] = module.params.get("sns_topic_arn")
    params["sns_topic_status"] = module.params.get("sns_topic_status")
    params["subnet_group_name"] = module.params.get("subnet_group_name")
    params["tags"] = module.params.get("tags")
    params["tls_enabled"] = module.params.get("tls_enabled")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alis from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "ClusterName",
        "TLSEnabled",
        "DataTiering",
        "KmsKeyId",
        "Port",
        "SubnetGroupName",
        "SnapshotArns",
        "SnapshotName",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["ClusterName"]

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
