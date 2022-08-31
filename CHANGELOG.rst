==========================
amazon.cloud Release Notes
==========================

.. contents:: Topics


v0.2.0
======

Minor Changes
-------------

- rdsdb_proxy - module renamed to ``rds_db_proxy``.
- s3_object_lambda_access_point - module renamed to ``s3objectlambda_access_point``.
- s3_object_lambda_access_point_policy - module renamed to ``s3objectlambda_access_point_policy``.

New Modules
-----------

- cloudtrail_event_data_store - Creates and manages a new event data store
- cloudtrail_trail - Creates and manages a trail that specifies the settings for delivery of log data to an Amazon S3 bucket.
- cloudwatch_composite_alarm - Creates and manages a composite alarm
- cloudwatch_metric_stream - Creates and manages a metric stream
- dynamodb_global_table - Creates and manages a Version 2019.11.21 global table
- eks_addon - Creates and manages Amazon EKS add-ons
- eks_fargate_profile - Creates and manage AWS Fargate profiles
- iam_server_certificate - Uploads and manages a server certificate entity for the AWS account
- kms_alias - Specifies a display name for a KMS key.
- kms_replica_key - Creates andn manages a multi-Region replica key that is based on a multi-Region primary key
- rds_db_proxy - Create and manage DB proxies
- rds_db_proxy_endpoint - Creates and manages a DB proxy endpoint
- redshift_endpoint_access - Creates and manages Redshift-managed VPC endpoint
- redshift_endpoint_authorization - Describes an endpoint authorization for authorizing Redshift-managed VPC endpoint access to a cluster across AWS accounts.
- redshift_scheduled_action - Creates and manages a scheduled action
- route53_dnssec - Is used to enable DNSSEC signing in a hosted zone
- route53_key_signing_key - Creates a new key-signing key (KSK) in a hosted zone
- s3objectlambda_access_point - Create and manage Object Lambda Access Points used to access S3 buckets
- s3objectlambda_access_point_policy - Specifies the Object Lambda Access Point resource policy document

v0.1.0
======

New Modules
-----------

- backup_backup_vault - Create and manage logical containers where backups are stored
- backup_framework - Create and manage frameworks with one or more controls
- backup_report_plan - Create and manage report plans
- eks_cluster - Create and manages Amazon EKS control planes
- iam_role - Create and manage roles
- lambda_code_signing_config - Code signing for AWS Lambda
- lambda_event_source_mapping - Create a mapping between an event source and an AWS Lambda function
- lambda_function - Create and manage Lambda functions
- logs_log_group - Create and manage log groups
- logs_query_definition - Create and manage query definitions
- logs_resource_policy - Create and manage resource policies
- rdsdb_proxy - Create and manage DB proxies
- redshift_cluster - Create and manage clusters
- redshift_event_subscription - Create and manage Amazon Redshift event notification subscriptions
- s3_access_point - Create and manage Amazon S3 access points to use to access S3 buckets
- s3_bucket - Create and manage S3 buckets
- s3_multi_region_access_point - Create and manage Amazon S3 Multi-Region Access Points
- s3_multi_region_access_point_policy - Manage Amazon S3 access policies
- s3_object_lambda_access_point - Create and manage Object Lambda Access Points used to access S3 buckets
- s3_object_lambda_access_point_policy - Specifies the Object Lambda Access Point resource policy document
