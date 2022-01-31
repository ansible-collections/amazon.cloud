#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from cmath import log
from dataclasses import replace

__metaclass__ = type

DOCUMENTATION = '''
---
module: s3_bucket
version_added: 3.0.0
short_description: Get info (List) about resources using the AWS Cloud API
description:
  - Get info (List) resources using the AWS Cloud API
options:
  role_arn:
    description:
      - The identifier of the resource. Gathers information on all resources by default.
    type: str
  client_token:
    description:
      - The identifier of the resource. Gathers information on all resources by default.
    type: str
  state:
    description:
      - The state operation to perform on the resource.
    choices:
      - create
      - delete
      - update
      - describe
      - list
    type: str
    default: create
  accelerate_configuration:
    type: str
  access_control:
    type: str
  analytics_configurations:
    type: str
  bucket_encryption:
    type: str
  bucket_name:
    type: str
  cors_configuration:
    type: str
  intelligent_tiering_configurations:
    type: str
  inventory_configurations:
    type: str
  lifecycle_configuration:
    type: str
  logging_configuration:
    type: str
  metrics_configurations:
    type: str
  notification_configuration:
    type: str
  object_lock_configuration:
    type: str
  object_lock_enabled:
    type: str
  ownership_controls:
    type: str
  public_access_block_configuration:
    type: str
  replication_configuration:
    type: str
  tags:
    type: str
  versioning_configuration:
    type: str
  website_configuration:
    type: str
  arn:
    type: str
  domain_name:
    type: str
  dual_stack_domain_name:
    type: str
  regional_domain_name:
    type: str
  website_url:
    type: str

author:
    - Jill Rouleau (@jillr)
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.

  - name: Create bucket
    amazon.cloud.s3_bucket:
      state: create
      bucket_name: '{{ bucket_name }}'

  - name: List all buckets
    amazon.cloud.s3_bucket:
      state: list

'''

try:
    import botocore
except ImportError:
    pass  # Handled by AnsibleAWSModule

import json
from ansible_collections.amazon.aws.plugins.module_utils.core import \
    AnsibleAWSModule
from ansible_collections.amazon.cloud.plugins.module_utils.core import CloudControlResource
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict, snake_dict_to_camel_dict


def main():
    argument_spec = dict(
        role_arn=dict(type='str'),
        client_token=dict(type='str', no_log=True),
        state=dict(type='str',
                   choices=['create', 'update', 'delete', 'list', 'describe'],
                   default='create'),
        accelerate_configuration=dict(type='str', required=False),
        access_control=dict(type='str', required=False),
        analytics_configurations=dict(type='str', required=False),
        bucket_encryption=dict(type='str', required=False),
        bucket_name=dict(type='str', required=False),
        cors_configuration=dict(type='str', required=False),
        intelligent_tiering_configurations=dict(type='str', required=False),
        inventory_configurations=dict(type='str', required=False),
        lifecycle_configuration=dict(type='str', required=False),
        logging_configuration=dict(type='str', required=False),
        metrics_configurations=dict(type='str', required=False),
        notification_configuration=dict(type='str', required=False),
        object_lock_configuration=dict(type='str', required=False),
        object_lock_enabled=dict(type='str', required=False),
        ownership_controls=dict(type='str', required=False),
        public_access_block_configuration=dict(type='dict', required=False),
        replication_configuration=dict(type='str', required=False),
        tags=dict(type='str', required=False),
        versioning_configuration=dict(type='str', required=False),
        website_configuration=dict(type='str', required=False),
        arn=dict(type='str', required=False),
        domain_name=dict(type='str', required=False),
        dual_stack_domain_name=dict(type='str', required=False),
        regional_domain_name=dict(type='str', required=False),
        website_url=dict(type='str', required=False),        
    )

    module = AnsibleAWSModule(argument_spec=argument_spec,
                              supports_check_mode=False)
    cloud = CloudControlResource(module)

    type_name = 'AWS::S3::Bucket'
    params = dict()

    params['AccelerateConfiguration'] = module.params.get(
        'accelerate_configuration')
    params['AccessControl'] = module.params.get('access_control')
    params['AnalyticsConfigurations'] = module.params.get(
        'analytics_configurations')
    params['BucketEncryption'] = module.params.get('bucket_encryption')
    params['BucketName'] = module.params.get('bucket_name')
    params['CorsConfiguration'] = module.params.get('cors_configuration')
    params['IntelligentTieringConfigurations'] = module.params.get(
        'intelligent_tiering_configurations')
    params['InventoryConfigurations'] = module.params.get(
        'inventory_configurations')
    params['LifecycleConfiguration'] = module.params.get(
        'lifecycle_configuration')
    params['LoggingConfiguration'] = module.params.get('logging_configuration')
    params['MetricsConfigurations'] = module.params.get(
        'metrics_configurations')
    params['NotificationConfiguration'] = module.params.get(
        'notification_configuration')
    params['ObjectLockConfiguration'] = module.params.get(
        'object_lock_configuration')
    params['ObjectLockEnabled'] = module.params.get('object_lock_enabled')
    params['OwnershipControls'] = module.params.get('ownership_controls')

    if module.params.get('public_access_block_configuration'):  # BlockPublicAcls, BlockPublicPolicy, IgnorePublicAcls, RestrictPublicBuckets, 
        params['PublicAccessBlockConfiguration'] = snake_dict_to_camel_dict(module.params.get('public_access_block_configuration'), capitalize_first=True)
  
    params['ReplicationConfiguration'] = module.params.get(
        'replication_configuration')
    params['Tags'] = module.params.get('tags')
    params['VersioningConfiguration'] = module.params.get(
        'versioning_configuration')
    params['WebsiteConfiguration'] = module.params.get('website_configuration')
    params['Arn'] = module.params.get('arn')
    params['DomainName'] = module.params.get('domain_name')
    params['DualStackDomainName'] = module.params.get('dual_stack_domain_name')
    params['RegionalDomainName'] = module.params.get('regional_domain_name')
    params['WebsiteURL'] = module.params.get('website_url')

    state = module.params.get('state')
    changed = False
    result = []

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    params_to_set = {k: v for k, v in params.items() if v is not None}
    desired_state = json.dumps(params_to_set)

    if state == 'list':
        result = cloud.list_resources(type_name)
        changed = False

    # RETURNED RESPONSE SNIPPET FROM S3_BUCKET
    #
    #     "ResourceDescriptions": [
    # {
    #     "Identifier": "ansible-test-jillr",
    #     "Properties": "{\"BucketName\":\"ansible-test-jillr\"}"
    # }
    # ]
    #

    if state == 'create':  # ConcurrentOperationException if try to create when previously tried to delete, add a waiter
        """
        {'ProgressEvent': {'EventTime': datetime.datetime(2022, 1, 6, 16, 14, 55, 315000, tzinfo=tzlocal()), 'Identifier': 'testdsbugvduskxcb', 'Operation': 'CREATE', 'OperationStatus': 'IN_PROGRESS', 'RequestToken': '0d4f4fb6-c360-4421-ac6c-f1a8cef71449', 'TypeName': 'AWS::S3::Bucket'}, 'ResponseMetadata': {'HTTPHeaders': {'content-length': '217', 'content-type': 'application/x-amz-json-1.0', 'date': 'Thu, 06 Jan 2022 23:14:55 GMT', 'x-amzn-requestid': 'fd6707d7-6301-49af-8272-d642f3d8c90c'}, 'HTTPStatusCode': 200, 'RequestId': 'fd6707d7-6301-49af-8272-d642f3d8c90c', 'RetryAttempts': 0}}
        """
        identifier = params['BucketName']
        result = cloud.create_resource(type_name, identifier, desired_state)
        #result = format_list(response)
            

    if state == 'update':
      # Get information about the current state of the specified resource.
      identifier = params['BucketName']
      result = cloud.update_resource(type_name, identifier, params_to_set)
      
    if state == 'delete':
      # Get information about the current state of the specified resource.
      identifier = params['BucketName']
      result = cloud.delete_resource(type_name, identifier)
      
      #result = format_list(response)

    # result = [camel_dict_to_snake_dict(result) for resource in response]

    module.exit_json(**result)


if __name__ == '__main__':
    main()
