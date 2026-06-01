from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, Mock

import pytest

from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    CloudControlResource,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    ansible_dict_to_boto3_tag_list,
)


@pytest.fixture
def ccr():
    class NotFound(Exception):
        pass

    module = Mock()
    module.check_mode = False
    module.params = {"wait_timeout": 5, "bucket_name": "test_bucket"}

    def _fail(*args, **kwargs):
        raise Exception("module exit")

    module.fail_json.side_effect = _fail
    module.fail_json_aws.side_effect = _fail

    resource = CloudControlResource(module)
    resource.client = MagicMock()
    resource.client.exceptions.ResourceNotFoundException = NotFound
    resource.client.list_resource_requests.return_value = {
        "ResourceRequestStatusSummaries": []
    }
    resource.client.update_resource.return_value = {
        "ProgressEvent": {
            "OperationStatus": "IN_PROGRESS",
            "RequestToken": "test-token",
        }
    }
    return resource


# Commented on because of
# NotImplementedError: Waiter resource_request_success could not be found for
# client <class 'unittest.mock.MagicMock'>. Available waiters: ('CloudControlApi', 'resource_request_success')
# It requires to wrap up the cloudcontrol client
# def test_present_creates_resource(ccr):
#     ccr.client.get_resource.side_effect = (
#         ccr.client.exceptions.ResourceNotFoundException()
#     )
#     params = {"BucketName": "test_bucket"}
#     changed = ccr.present("AWS::S3::Bucket", "test_bucket", params)
#     assert changed
#     ccr.client.create_resource.assert_called_with(
#         TypeName="AWS::S3::Bucket", DesiredState=json.dumps(params)
#     )
#     ccr.client.update_resource.assert_not_called()


def test_present_updates_resource(ccr):
    resource = {
        "TypeName": "AWS::S3::Bucket",
        "ResourceDescription": {
            "Identifier": "test_bucket",
            "Properties": '{"BucketName": "test_bucket"}',
        },
    }
    ccr.client.get_resource.return_value = resource
    create_only_params = []
    params = {"BucketName": "test_bucket", "Tags": [{"Key": "k", "Value": "v"}]}
    results = ccr.present(
        "AWS::S3::Bucket", ["bucket_name"], params, create_only_params
    )
    assert results["changed"]
    ccr.client.update_resource.assert_called_with(
        TypeName="AWS::S3::Bucket",
        Identifier="test_bucket",
        PatchDocument='[{"op": "add", "path": "/Tags", "value": [{"Key": "k", "Value": "v"}]}]',
        aws_retry=True,
    )
    ccr.client.create_resource.assert_not_called()


def test_absent_deletes_resource(ccr):
    resource = {
        "TypeName": "AWS::S3::Bucket",
        "ResourceDescription": {
            "Identifier": "test_bucket",
            "Properties": '{"BucketName": "test_bucket"}',
        },
    }
    ccr.client.get_resource.return_value = resource
    ccr.module.params = {"wait_timeout": 5, "bucket_name": "test_bucket"}
    changed = ccr.absent("AWS::S3::Bucket", ["bucket_name"])
    assert changed
    ccr.client.delete_resource.assert_called_with(
        TypeName="AWS::S3::Bucket",
        Identifier="test_bucket",
        aws_retry=True,
    )
    ccr.client.create_resource.assert_not_called()
    ccr.client.update_resource.assert_not_called()


def test_absent_deletes_resource_NotFound(ccr):
    ccr.client.get_resource.side_effect = (
        ccr.client.exceptions.ResourceNotFoundException()
    )
    ccr.module.params = {"wait_timeout": 5, "bucket_name": "test_bucket"}
    changed = ccr.absent("AWS::S3::Bucket", ["bucket_name"])
    assert changed is False
    ccr.client.delete_resource.assert_not_called()
    ccr.client.create_resource.assert_not_called()
    ccr.client.update_resource.assert_not_called()


def test__ansible_dict_to_boto3_tag_list():
    tags_dict = {
        "lowerCamel": "lowerCamelValue",
        "UpperCamel": "upperCamelValue",
        "Normal case": "Normal Value",
        "lower case": "lower case value",
    }
    expected = [
        {"Key": "lowerCamel", "Value": "lowerCamelValue"},
        {"Key": "UpperCamel", "Value": "upperCamelValue"},
        {"Key": "Normal case", "Value": "Normal Value"},
        {"Key": "lower case", "Value": "lower case value"},
    ]
    converted_list = ansible_dict_to_boto3_tag_list(tags_dict)
    sorted_converted_list = sorted(converted_list, key=lambda i: (i["Key"]))
    sorted_list = sorted(expected, key=lambda i: (i["Key"]))
    assert sorted_converted_list == sorted_list
