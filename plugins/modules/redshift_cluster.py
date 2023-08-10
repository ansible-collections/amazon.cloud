#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: redshift_cluster
short_description: Create and manage clusters
description:
- Creates and manage clusters.
options:
    allow_version_upgrade:
        aliases:
        - AllowVersionUpgrade
        description:
        - Major version upgrades can be applied during the maintenance window to the
            Amazon Redshift engine that is running on the cluster.
        - Default value is True.
        type: bool
    aqua_configuration_status:
        aliases:
        - AquaConfigurationStatus
        description:
        - The value represents how the cluster is configured to use AQUA (Advanced
            Query Accelerator) after the cluster is restored.
        - Possible values include the following.
        - enabled - Use AQUA if it is available for the current Region and Amazon
            Redshift node type.
        - disabled - Dont use AQUA.
        - auto - Amazon Redshift determines whether to use AQUA.
        type: str
    automated_snapshot_retention_period:
        aliases:
        - AutomatedSnapshotRetentionPeriod
        description:
        - The number of days that automated snapshots are retained.
        - If the value is 0, automated snapshots are disabled.
        - Default value is 1.
        type: int
    availability_zone:
        aliases:
        - AvailabilityZone
        description:
        - The EC2 Availability Zone (AZ) in which you want Amazon Redshift to provision
            the cluster.
        - 'Default: A random, system-chosen Availability Zone in the region that is
            specified by the endpoint.'
        type: str
    availability_zone_relocation:
        aliases:
        - AvailabilityZoneRelocation
        description:
        - The option to enable relocation for an Amazon Redshift cluster between Availability
            Zones after the cluster modification is complete.
        type: bool
    availability_zone_relocation_status:
        aliases:
        - AvailabilityZoneRelocationStatus
        description:
        - The availability zone relocation status of the cluster.
        type: str
    classic:
        aliases:
        - Classic
        description:
        - A boolean value indicating whether the resize operation is using the classic
            resize process.
        - If you dont provide this parameter or set the value to false , the resize
            type is elastic.
        type: bool
    cluster_identifier:
        aliases:
        - ClusterIdentifier
        description:
        - A unique identifier for the cluster.
        - You use this identifier to refer to the cluster for any subsequent cluster
            operations such as deleting or modifying.
        - All alphabetical characters must be lower case, no hypens at the end, no
            two consecutive hyphens.
        - Cluster name should be unique for all clusters within an AWS account.
        type: str
    cluster_parameter_group_name:
        aliases:
        - ClusterParameterGroupName
        description:
        - The name of the parameter group to be associated with this cluster.
        type: str
    cluster_security_groups:
        aliases:
        - ClusterSecurityGroups
        description:
        - A list of security groups to be associated with this cluster.
        elements: str
        type: list
    cluster_subnet_group_name:
        aliases:
        - ClusterSubnetGroupName
        description:
        - The name of a cluster subnet group to be associated with this cluster.
        type: str
    cluster_type:
        aliases:
        - ClusterType
        description:
        - The type of the cluster.
        - When cluster type is specified as single-node, the NumberOfNodes parameter
            is not required and if multi-node, the NumberOfNodes parameter is required.
        type: str
    cluster_version:
        aliases:
        - ClusterVersion
        description:
        - The version of the Amazon Redshift engine software that you want to deploy
            on the cluster.The version selected runs on all the nodes in the cluster.
        type: str
    db_name:
        aliases:
        - DBName
        description:
        - The name of the first database to be created when the cluster is created.
        - To create additional databases after the cluster is created, connect to
            the cluster with a SQL client and use SQL commands to create a database.
        type: str
    defer_maintenance:
        aliases:
        - DeferMaintenance
        description:
        - A boolean indicating whether to enable the deferred maintenance window.
        type: bool
    defer_maintenance_duration:
        aliases:
        - DeferMaintenanceDuration
        description:
        - An integer indicating the duration of the maintenance window in days.
        - If you specify a duration, you cant specify an end time.
        - The duration must be 45 days or less.
        type: int
    defer_maintenance_end_time:
        aliases:
        - DeferMaintenanceEndTime
        description:
        - A timestamp indicating end time for the deferred maintenance window.
        - If you specify an end time, you cant specify a duration.
        type: str
    defer_maintenance_start_time:
        aliases:
        - DeferMaintenanceStartTime
        description:
        - A timestamp indicating the start time for the deferred maintenance window.
        type: str
    destination_region:
        aliases:
        - DestinationRegion
        description:
        - The destination AWS Region that you want to copy snapshots to.
        - 'Constraints: Must be the name of a valid AWS Region.'
        - For more information, see Regions and Endpoints in the Amazon Web Services
            ) General Reference.
        type: str
    elastic_ip:
        aliases:
        - ElasticIp
        description:
        - The Elastic IP (EIP) address for the cluster.
        type: str
    encrypted:
        aliases:
        - Encrypted
        description:
        - If true, the data in the cluster is encrypted at rest.
        type: bool
    enhanced_vpc_routing:
        aliases:
        - EnhancedVpcRouting
        description:
        - An option that specifies whether to create the cluster with enhanced VPC
            routing enabled.
        - To create a cluster that uses enhanced VPC routing, the cluster must be
            in a VPC. For more information, see Enhanced VPC Routing in the Amazon
            Redshift Cluster Management Guide.
        - If this option is true , enhanced VPC routing is enabled.
        - 'Default: false.'
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
    hsm_client_certificate_identifier:
        aliases:
        - HsmClientCertificateIdentifier
        description:
        - Specifies the name of the HSM client certificate the Amazon Redshift cluster
            uses to retrieve the data encryption keys stored in an HSM.
        type: str
    hsm_configuration_identifier:
        aliases:
        - HsmConfigurationIdentifier
        description:
        - Specifies the name of the HSM configuration that contains the information
            the Amazon Redshift cluster can use to retrieve and store keys in an HSM.
        type: str
    iam_roles:
        aliases:
        - IamRoles
        description:
        - A list of AWS Identity and Access Management (IAM) roles that can be used
            by the cluster to access other AWS services.
        - You must supply the IAM roles in their Amazon Resource Name (ARN) format.
        - You can supply up to 50 IAM roles in a single request.
        elements: str
        type: list
    kms_key_id:
        aliases:
        - KmsKeyId
        description:
        - The AWS Key Management Service (KMS) key ID of the encryption key that you
            want to use to encrypt data in the cluster.
        type: str
    logging_properties:
        aliases:
        - LoggingProperties
        description:
        - Not Provived.
        suboptions:
            bucket_name:
                aliases:
                - BucketName
                description:
                - Not Provived.
                type: str
            s3_key_prefix:
                aliases:
                - S3KeyPrefix
                description:
                - Not Provived.
                type: str
        type: dict
    maintenance_track_name:
        aliases:
        - MaintenanceTrackName
        description:
        - The name for the maintenance track that you want to assign for the cluster.
        - This name change is asynchronous.
        - The new track name stays in the PendingModifiedValues for the cluster until
            the next maintenance window.
        - When the maintenance track changes, the cluster is switched to the latest
            cluster release available for the maintenance track.
        - At this point, the maintenance track name is applied.
        type: str
    manual_snapshot_retention_period:
        aliases:
        - ManualSnapshotRetentionPeriod
        description:
        - The number of days to retain newly copied snapshots in the destination AWS
            Region after they are copied from the source AWS Region.
        - If the value is -1, the manual snapshot is retained indefinitely.
        - The value must be either -1 or an integer between 1 and 3,653.
        type: int
    master_user_password:
        aliases:
        - MasterUserPassword
        description:
        - The password associated with the master user account for the cluster that
            is being created.
        - Password must be between 8 and 64 characters in length, should have at least
            one uppercase letter.Must contain at least one lowercase letter.Must contain
            one number.Can be any printable ASCII character.
        type: str
    master_username:
        aliases:
        - MasterUsername
        description:
        - The user name associated with the master user account for the cluster that
            is being created.
        - The user name cant be PUBLIC and first character must be a letter.
        type: str
    node_type:
        aliases:
        - NodeType
        description:
        - 'The node type to be provisioned for the cluster.Valid Values: ds2.xlarge
            | ds2.8xlarge | dc1.large | dc1.8xlarge | dc2.large | dc2.8xlarge | ra3.4xlarge
            | ra3.16xlarge.'
        type: str
    number_of_nodes:
        aliases:
        - NumberOfNodes
        description:
        - The number of compute nodes in the cluster.
        - This parameter is required when the ClusterType parameter is specified as
            multi-node.
        type: int
    owner_account:
        aliases:
        - OwnerAccount
        description:
        - Not Provived.
        type: str
    port:
        aliases:
        - Port
        description:
        - The port number on which the cluster accepts incoming connections.
        - The cluster is accessible only via the JDBC and ODBC connection strings.
        type: int
    preferred_maintenance_window:
        aliases:
        - PreferredMaintenanceWindow
        description:
        - The weekly time range (in UTC) during which automated cluster maintenance
            can occur.
        type: str
    publicly_accessible:
        aliases:
        - PubliclyAccessible
        description:
        - If true, the cluster can be accessed from a public network.
        type: bool
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    resource_action:
        aliases:
        - ResourceAction
        description:
        - The Redshift operation to be performed.
        - Resource Action supports pause-cluster, resume-cluster APIs.
        type: str
    revision_target:
        aliases:
        - RevisionTarget
        description:
        - The identifier of the database revision.
        - You can retrieve this value from the response to the DescribeClusterDbRevisions
            request.
        type: str
    rotate_encryption_key:
        aliases:
        - RotateEncryptionKey
        description:
        - A boolean indicating if we want to rotate Encryption Keys.
        type: bool
    snapshot_cluster_identifier:
        aliases:
        - SnapshotClusterIdentifier
        description:
        - The name of the cluster the source snapshot was created from.
        - This parameter is required if your IAM user has a policy containing a snapshot
            resource element that specifies anything other than * for the cluster
            name.
        type: str
    snapshot_copy_grant_name:
        aliases:
        - SnapshotCopyGrantName
        description:
        - The name of the snapshot copy grant to use when snapshots of an AWS KMS-encrypted
            cluster are copied to the destination region.
        type: str
    snapshot_copy_manual:
        aliases:
        - SnapshotCopyManual
        description:
        - Indicates whether to apply the snapshot retention period to newly copied
            manual snapshots instead of automated snapshots.
        type: bool
    snapshot_copy_retention_period:
        aliases:
        - SnapshotCopyRetentionPeriod
        description:
        - The number of days to retain automated snapshots in the destination region
            after they are copied from the source region.
        - Default is 7.
        - 'Constraints: Must be at least 1 and no more than 35.'
        type: int
    snapshot_identifier:
        aliases:
        - SnapshotIdentifier
        description:
        - The name of the snapshot from which to create the new cluster.
        - This parameter isnt case sensitive.
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
    vpc_security_group_ids:
        aliases:
        - VpcSecurityGroupIds
        description:
        - A list of Virtual Private Cloud (VPC) security groups to be associated with
            the cluster.
        elements: str
        type: list
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

    argument_spec["cluster_identifier"] = {
        "type": "str",
        "aliases": ["ClusterIdentifier"],
    }
    argument_spec["master_username"] = {"type": "str", "aliases": ["MasterUsername"]}
    argument_spec["master_user_password"] = {
        "type": "str",
        "aliases": ["MasterUserPassword"],
    }
    argument_spec["node_type"] = {"type": "str", "aliases": ["NodeType"]}
    argument_spec["allow_version_upgrade"] = {
        "type": "bool",
        "aliases": ["AllowVersionUpgrade"],
    }
    argument_spec["automated_snapshot_retention_period"] = {
        "type": "int",
        "aliases": ["AutomatedSnapshotRetentionPeriod"],
    }
    argument_spec["availability_zone"] = {
        "type": "str",
        "aliases": ["AvailabilityZone"],
    }
    argument_spec["cluster_parameter_group_name"] = {
        "type": "str",
        "aliases": ["ClusterParameterGroupName"],
    }
    argument_spec["cluster_type"] = {"type": "str", "aliases": ["ClusterType"]}
    argument_spec["cluster_version"] = {"type": "str", "aliases": ["ClusterVersion"]}
    argument_spec["cluster_subnet_group_name"] = {
        "type": "str",
        "aliases": ["ClusterSubnetGroupName"],
    }
    argument_spec["db_name"] = {"type": "str", "aliases": ["DBName"]}
    argument_spec["elastic_ip"] = {"type": "str", "aliases": ["ElasticIp"]}
    argument_spec["encrypted"] = {"type": "bool", "aliases": ["Encrypted"]}
    argument_spec["hsm_client_certificate_identifier"] = {
        "type": "str",
        "aliases": ["HsmClientCertificateIdentifier"],
    }
    argument_spec["hsm_configuration_identifier"] = {
        "type": "str",
        "aliases": ["HsmConfigurationIdentifier"],
    }
    argument_spec["kms_key_id"] = {"type": "str", "aliases": ["KmsKeyId"]}
    argument_spec["number_of_nodes"] = {"type": "int", "aliases": ["NumberOfNodes"]}
    argument_spec["port"] = {"type": "int", "aliases": ["Port"]}
    argument_spec["preferred_maintenance_window"] = {
        "type": "str",
        "aliases": ["PreferredMaintenanceWindow"],
    }
    argument_spec["publicly_accessible"] = {
        "type": "bool",
        "aliases": ["PubliclyAccessible"],
    }
    argument_spec["cluster_security_groups"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["ClusterSecurityGroups"],
    }
    argument_spec["iam_roles"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["IamRoles"],
    }
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags", "resource_tags"]}
    argument_spec["vpc_security_group_ids"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["VpcSecurityGroupIds"],
    }
    argument_spec["snapshot_cluster_identifier"] = {
        "type": "str",
        "aliases": ["SnapshotClusterIdentifier"],
    }
    argument_spec["snapshot_identifier"] = {
        "type": "str",
        "aliases": ["SnapshotIdentifier"],
    }
    argument_spec["owner_account"] = {"type": "str", "aliases": ["OwnerAccount"]}
    argument_spec["logging_properties"] = {
        "type": "dict",
        "options": {
            "bucket_name": {"type": "str", "aliases": ["BucketName"]},
            "s3_key_prefix": {"type": "str", "aliases": ["S3KeyPrefix"]},
        },
        "aliases": ["LoggingProperties"],
    }
    argument_spec["destination_region"] = {
        "type": "str",
        "aliases": ["DestinationRegion"],
    }
    argument_spec["snapshot_copy_retention_period"] = {
        "type": "int",
        "aliases": ["SnapshotCopyRetentionPeriod"],
    }
    argument_spec["snapshot_copy_grant_name"] = {
        "type": "str",
        "aliases": ["SnapshotCopyGrantName"],
    }
    argument_spec["manual_snapshot_retention_period"] = {
        "type": "int",
        "aliases": ["ManualSnapshotRetentionPeriod"],
    }
    argument_spec["snapshot_copy_manual"] = {
        "type": "bool",
        "aliases": ["SnapshotCopyManual"],
    }
    argument_spec["availability_zone_relocation"] = {
        "type": "bool",
        "aliases": ["AvailabilityZoneRelocation"],
    }
    argument_spec["availability_zone_relocation_status"] = {
        "type": "str",
        "aliases": ["AvailabilityZoneRelocationStatus"],
    }
    argument_spec["aqua_configuration_status"] = {
        "type": "str",
        "aliases": ["AquaConfigurationStatus"],
    }
    argument_spec["classic"] = {"type": "bool", "aliases": ["Classic"]}
    argument_spec["enhanced_vpc_routing"] = {
        "type": "bool",
        "aliases": ["EnhancedVpcRouting"],
    }
    argument_spec["maintenance_track_name"] = {
        "type": "str",
        "aliases": ["MaintenanceTrackName"],
    }
    argument_spec["defer_maintenance"] = {
        "type": "bool",
        "aliases": ["DeferMaintenance"],
    }
    argument_spec["defer_maintenance_start_time"] = {
        "type": "str",
        "aliases": ["DeferMaintenanceStartTime"],
    }
    argument_spec["defer_maintenance_end_time"] = {
        "type": "str",
        "aliases": ["DeferMaintenanceEndTime"],
    }
    argument_spec["defer_maintenance_duration"] = {
        "type": "int",
        "aliases": ["DeferMaintenanceDuration"],
    }
    argument_spec["revision_target"] = {"type": "str", "aliases": ["RevisionTarget"]}
    argument_spec["resource_action"] = {"type": "str", "aliases": ["ResourceAction"]}
    argument_spec["rotate_encryption_key"] = {
        "type": "bool",
        "aliases": ["RotateEncryptionKey"],
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
        [
            "state",
            "present",
            [
                "cluster_identifier",
                "master_user_password",
                "master_username",
                "db_name",
                "cluster_type",
                "node_type",
            ],
            True,
        ],
        ["state", "absent", ["cluster_identifier"], True],
        ["state", "get", ["cluster_identifier"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::Redshift::Cluster"

    params = {}

    params["allow_version_upgrade"] = module.params.get("allow_version_upgrade")
    params["aqua_configuration_status"] = module.params.get("aqua_configuration_status")
    params["automated_snapshot_retention_period"] = module.params.get(
        "automated_snapshot_retention_period"
    )
    params["availability_zone"] = module.params.get("availability_zone")
    params["availability_zone_relocation"] = module.params.get(
        "availability_zone_relocation"
    )
    params["availability_zone_relocation_status"] = module.params.get(
        "availability_zone_relocation_status"
    )
    params["classic"] = module.params.get("classic")
    params["cluster_identifier"] = module.params.get("cluster_identifier")
    params["cluster_parameter_group_name"] = module.params.get(
        "cluster_parameter_group_name"
    )
    params["cluster_security_groups"] = module.params.get("cluster_security_groups")
    params["cluster_subnet_group_name"] = module.params.get("cluster_subnet_group_name")
    params["cluster_type"] = module.params.get("cluster_type")
    params["cluster_version"] = module.params.get("cluster_version")
    params["db_name"] = module.params.get("db_name")
    params["defer_maintenance"] = module.params.get("defer_maintenance")
    params["defer_maintenance_duration"] = module.params.get(
        "defer_maintenance_duration"
    )
    params["defer_maintenance_end_time"] = module.params.get(
        "defer_maintenance_end_time"
    )
    params["defer_maintenance_start_time"] = module.params.get(
        "defer_maintenance_start_time"
    )
    params["destination_region"] = module.params.get("destination_region")
    params["elastic_ip"] = module.params.get("elastic_ip")
    params["encrypted"] = module.params.get("encrypted")
    params["enhanced_vpc_routing"] = module.params.get("enhanced_vpc_routing")
    params["hsm_client_certificate_identifier"] = module.params.get(
        "hsm_client_certificate_identifier"
    )
    params["hsm_configuration_identifier"] = module.params.get(
        "hsm_configuration_identifier"
    )
    params["iam_roles"] = module.params.get("iam_roles")
    params["kms_key_id"] = module.params.get("kms_key_id")
    params["logging_properties"] = module.params.get("logging_properties")
    params["maintenance_track_name"] = module.params.get("maintenance_track_name")
    params["manual_snapshot_retention_period"] = module.params.get(
        "manual_snapshot_retention_period"
    )
    params["master_user_password"] = module.params.get("master_user_password")
    params["master_username"] = module.params.get("master_username")
    params["node_type"] = module.params.get("node_type")
    params["number_of_nodes"] = module.params.get("number_of_nodes")
    params["owner_account"] = module.params.get("owner_account")
    params["port"] = module.params.get("port")
    params["preferred_maintenance_window"] = module.params.get(
        "preferred_maintenance_window"
    )
    params["publicly_accessible"] = module.params.get("publicly_accessible")
    params["resource_action"] = module.params.get("resource_action")
    params["revision_target"] = module.params.get("revision_target")
    params["rotate_encryption_key"] = module.params.get("rotate_encryption_key")
    params["snapshot_cluster_identifier"] = module.params.get(
        "snapshot_cluster_identifier"
    )
    params["snapshot_copy_grant_name"] = module.params.get("snapshot_copy_grant_name")
    params["snapshot_copy_manual"] = module.params.get("snapshot_copy_manual")
    params["snapshot_copy_retention_period"] = module.params.get(
        "snapshot_copy_retention_period"
    )
    params["snapshot_identifier"] = module.params.get("snapshot_identifier")
    params["tags"] = module.params.get("tags")
    params["vpc_security_group_ids"] = module.params.get("vpc_security_group_ids")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/ClusterIdentifier",
        "/properties/OwnerAccount",
        "/properties/SnapshotIdentifier",
        "/properties/DBName",
        "/properties/SnapshotClusterIdentifier",
        "/properties/ClusterSubnetGroupName",
        "/properties/MasterUsername",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/ClusterIdentifier"]

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
