# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2021 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This module_utility adds shared support for AWS Cloud Control API modules.
"""

import json
import time
import traceback
from itertools import count
from typing import Iterable, List, Dict, Optional, Union

from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.common import (
    set_collection_info,
)
from .utils import (
    normalize_response,
    scrub_keys,
    to_sync,
    to_async,
    ansible_dict_to_boto3_tag_list,
    snake_dict_to_camel_dict,
    diff_dicts,
    snake_to_camel,
    json_patch,
    get_patch,
)

from ansible_collections.amazon.cloud.plugins.module_utils.waiters import get_waiter

BOTO3_IMP_ERR = None
try:
    import botocore

    HAS_BOTO3 = True
except ImportError:
    BOTO3_IMP_ERR = traceback.format_exc()
    HAS_BOTO3 = False

AMAZON_CLOUD_COLLECTION_NAME = "amazon.cloud"
AMAZON_CLOUD_COLLECTION_VERSION = "0.2.0"


class CloudControlResource(object):
    def __init__(self, module):
        """
        Until we can use a connection plugin for auth and client setup, reuse AnsibleAWSModule
        """
        self.module = module
        self.client = module.client(
            "cloudcontrol", retry_decorator=AWSRetry.jittered_backoff(retries=10)
        )

    @property
    def _waiter_config(self):
        delay = min(10, self.module.params.get("wait_timeout"))
        max_attempts = self.module.params.get("wait_timeout") // delay
        return {"Delay": delay, "MaxAttempts": max_attempts}

    def wait_until_resource_request_success(self, request_token: str):
        try:
            # This waiter 'resource_request_success' only waits to reach SUCCESS status. It fails otherwise.
            # botocore.exceptions.WaiterError: Waiter ResourceRequestSuccess failed: Waiter encountered a terminal failure
            # state: For expression "ProgressEvent.OperationStatus" we matched expected path: CANCEL_COMPLETE
            # See https://github.com/boto/botocore/blob/develop/botocore/data/cloudcontrol/2021-09-30/waiters-2.json
            # We should wait for CANCEL_IN_PROGRESS and reach CANCEL_COMPLETE before updating.
            # Fall to a custom waiter.
            #
            # self.client.get_waiter("resource_request_success").wait(
            #    RequestToken=request_token,
            #    WaiterConfig=self._waiter_config,
            # )
            get_waiter(self.client, "resource_request_success").wait(
                RequestToken=request_token,
                WaiterConfig=self._waiter_config,
            )
        except botocore.exceptions.WaiterError as e:
            self.module.fail_json_aws(
                e.last_response["ProgressEvent"]["StatusMessage"],
                msg="Resource request failed to reach successful state",
            )
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            self.module.fail_json_aws(
                e, msg="Unable to wait for the resource request to become successful"
            )

    @to_sync
    @AWSRetry.jittered_backoff(
        catch_extra_error_codes=["ThrottlingException"], retries=10
    )
    async def list_resources(
        self, type_name: str, identifiers: Optional[List] = None
    ) -> List:
        """
        An exception occurred during task execution. To see the full traceback, use -vvv.
        The error was: botocore.exceptions.OperationNotPageableError: Operation cannot be paginated: list_resources
        Fall to manual pagination
        """
        resource_list: List = []
        results: List = []
        response: Dict = {}

        for i in count():
            # https://docs.aws.amazon.com/cloudcontrolapi/latest/APIReference/API_ListResources.html
            params = {
                # https://docs.aws.amazon.com/cloudcontrolapi/latest/userguide/supported-resources.html
                "TypeName": type_name,
            }
            # When a resource is identified using compound identifiers
            if identifiers:
                additional_properties: Dict = {}
                for id in identifiers:
                    additional_properties[
                        snake_to_camel(id, capitalize_first=True)
                    ] = self.module.params.get(id)
                params["ResourceModel"] = json.dumps(additional_properties)

            if i == 0 or "NextToken" in response:
                if "NextToken" in response:
                    params["NextToken"] = response["NextToken"]
                try:
                    response = self.client.list_resources(**params, aws_retry=True)
                except (
                    botocore.exceptions.BotoCoreError,
                    botocore.exceptions.ClientError,
                ) as e:
                    self.module.fail_json_aws(e, msg="Failed to list resources")
                # results.extend(normalize_response(response))
                resource_list.append(response)
            else:
                break

        for each in resource_list:
            resource_descriptions = each.get("ResourceDescriptions", [])

            # for r in resource_descriptions:
            #    identifier = r.get("Identifier")
            #    results.append(self.get_resource(type_name, identifier))

            # Fall to use asyncio to speed up the process
            import asyncio

            futures = [
                self.get_resources_async(type_name, r.get("Identifier"))
                for r in resource_descriptions
            ]
            results = await asyncio.gather(*futures)

        return results

    @AWSRetry.jittered_backoff(
        catch_extra_error_codes=["ThrottlingException"], retries=10
    )
    def list_resource_requests(self, params: Iterable) -> List:
        """
        Returns existing resource operation requests using specific filters.
        """
        results: List = []
        response: Dict = {}

        for i in count():
            # https://docs.aws.amazon.com/cloudcontrolapi/latest/APIReference/API_ListResourceRequests.html
            if i == 0 or "NextToken" in response:
                if "NextToken" in response:
                    params["NextToken"] = response["NextToken"]
                try:
                    response = self.client.list_resource_requests(
                        **params, aws_retry=True
                    )
                except (
                    botocore.exceptions.BotoCoreError,
                    botocore.exceptions.ClientError,
                ) as e:
                    self.module.fail_json_aws(e, msg="Failed to list resource requests")
                results.extend(response["ResourceRequestStatusSummaries"])
            else:
                break

        return results

    @to_async
    def get_resources_async(self, type_name, identifier):
        return self.get_resource(type_name, identifier)

    def get_resource(
        self, type_name: str, primary_identifier: Union[str, List, Dict]
    ) -> List:
        # This is the "describe" equivalent for AWS Cloud Control API
        response: Dict = {}
        identifier: Dict = {}

        if isinstance(primary_identifier, list):
            for id in primary_identifier:
                identifier[
                    snake_to_camel(id, capitalize_first=True)
                ] = self.module.params.get(id)
            primary_identifier = json.dumps(identifier)
        elif isinstance(primary_identifier, dict):
            primary_identifier = json.dumps(primary_identifier)

        try:
            response = self.client.get_resource(
                TypeName=type_name, Identifier=primary_identifier, aws_retry=True
            )
        except self.client.exceptions.ResourceNotFoundException:
            return response
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            self.module.fail_json_aws(e, msg="Failed to retrieve resource")

        result: List = normalize_response(response)

        return result

    def present(
        self,
        type_name: str,
        primary_identifier: List,
        params: Dict,
        create_only_params: List,
    ) -> bool:
        results = {"changed": False, "result": {}}
        create_only_params = create_only_params or []
        identifier: Dict = {}

        resource = None

        if self.module.params.get("identifier"):
            identifier = self.module.params.get("identifier")
        else:
            for id in primary_identifier:
                identifier[
                    snake_to_camel(id, capitalize_first=True)
                ] = self.module.params.get(id)
            identifier = json.dumps(identifier)

        try:
            resource = self.client.get_resource(
                TypeName=type_name, Identifier=identifier, aws_retry=True
            )
            results = self.update_resource(resource, params, create_only_params)
        except self.client.exceptions.ResourceNotFoundException:
            if self.module.params.get("identifier"):
                self.module.fail_json(
                    f"""You must specify both {*primary_identifier, } to create a new resource.
                        The identifier parameter can only be used to manipulate an existing resource."""
                )
            results["changed"] |= self.create_resource(type_name, params)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            self.module.fail_json_aws(e, msg="Failed to modify resource")

        results["result"] = self.get_resource(type_name, identifier)

        return results

    def create_resource(self, type_name: str, params: Dict) -> bool:
        changed: bool = False
        params = json.dumps(params)

        if not self.module.check_mode:
            try:
                response = self.client.create_resource(
                    TypeName=type_name, DesiredState=params
                )
            except (
                botocore.exceptions.BotoCoreError,
                botocore.exceptions.ClientError,
            ) as e:
                self.module.fail_json_aws(e, msg="Failed to create resource")

            self.wait_until_resource_request_success(
                response["ProgressEvent"]["RequestToken"]
            )
        changed: bool = True

        return changed

    def check_in_progress_requests(self, type_name: str, identifier: str):
        in_progress_requests: List = []
        params = {
            "ResourceRequestStatusFilter": {
                "Operations": ["CREATE", "DELETE", "UPDATE"],
                "OperationStatuses": [
                    "IN_PROGRESS",
                    "PENDING",
                ],
            }
        }

        response = self.list_resource_requests(params)

        if response:
            in_progress_requests = list(
                filter(
                    lambda d: d["TypeName"] == type_name
                    and d["Identifier"] == identifier,
                    response,
                )
            )
        return in_progress_requests

    def wait_for_in_progress_requests(
        self, in_progress_requests: List, identifier: str
    ):
        # Dont warn if nothing to wait on
        if in_progress_requests:
            self.module.warn(
                f"There is one or more IN PROGRESS operations on {identifier}. Wait until there are no more IN PROGRESS operations before proceding."
            )
            [
                self.wait_until_resource_request_success(e["RequestToken"])
                for e in in_progress_requests
            ]

    def absent(self, type_name: str, primary_identifier: List):
        changed: bool = False
        identifier: Dict = {}
        response: Dict = {}

        if self.module.params.get("identifier"):
            identifier = self.module.params.get("identifier")
        else:
            for id in primary_identifier:
                identifier[
                    snake_to_camel(id, capitalize_first=True)
                ] = self.module.params.get(id)
            identifier = json.dumps(identifier)

        try:
            response = self.client.get_resource(
                TypeName=type_name, Identifier=identifier, aws_retry=True
            )
        except self.client.exceptions.ResourceNotFoundException:
            return changed
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            self.module.fail_json_aws(e, msg="Failed to retrieve resource")
        else:
            return self.delete_resource(
                type_name, response["ResourceDescription"]["Identifier"]
            )

    def delete_resource(self, type_name: str, identifier: str) -> bool:
        changed: bool = True
        in_progress_requests: List = []

        in_progress_requests = self.check_in_progress_requests(type_name, identifier)
        # There is already a delete operation IN PROGRESS
        if any(
            filter(
                lambda d: d["Operation"] == "DELETE",
                in_progress_requests,
            )
        ):
            changed = False

        if self.module.check_mode:
            return changed

        self.wait_for_in_progress_requests(in_progress_requests, identifier)
        try:
            response = self.client.delete_resource(
                TypeName=type_name, Identifier=identifier, aws_retry=True
            )
        except self.client.exceptions.ResourceNotFoundException:
            # If the resource has been deleted by an IN PROGRESS delete operation
            return changed
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            self.module.fail_json_aws(e, msg="Failed to delete resource")

        if self.module.params.get("wait"):
            self.wait_until_resource_request_success(
                response["ProgressEvent"]["RequestToken"]
            )

        return changed

    def ensure_request_status(self, response: Dict) -> bool:
        # Wait until reource request becomes IN_PROGRESS
        time_end = time.time() + self.module.params.get("wait_timeout")
        delay = 15

        while time.time() < time_end:
            if response and response["ProgressEvent"]["OperationStatus"] == "PENDING":
                try:
                    response = self.client.get_resource_request_status(
                        RequestToken=response["ProgressEvent"]["RequestToken"],
                        aws_retry=True,
                    )
                except (
                    botocore.exceptions.BotoCoreError,
                    botocore.exceptions.ClientError,
                ) as e:
                    self.module.fail_json_aws(
                        e, msg="Failed to get resource request status"
                    )
            else:
                return
            time.sleep(delay)

        # Timeout occured
        self.module.fail_json(msg="Timeout occured waiting for resource request")

    def update_resource(
        self,
        resource: Dict,
        params_to_set: Dict,
        create_only_params: List,
    ) -> bool:
        identifier = resource["ResourceDescription"]["Identifier"]
        type_name = resource["TypeName"]
        properties = json.loads(resource["ResourceDescription"]["Properties"])
        results: Dict = {"changed": False, "result": []}
        obj = None

        # Ignore createOnlyProperties that can be set only during resource creation
        params = scrub_keys(
            params_to_set,
            [
                snake_to_camel(elem, capitalize_first=True)
                for elem in create_only_params
            ],
        )

        in_progress_requests = self.check_in_progress_requests(type_name, identifier)

        if not self.module.check_mode:
            if self.module.params.get("force"):
                self.module.warn(
                    f"There is one or more IN PROGRESS or PENDING resource requests on {identifier} that will be cancelled."
                )
                try:
                    for e in in_progress_requests:
                        self.client.cancel_resource_request(
                            RequestToken=e["RequestToken"], aws_retry=True
                        )
                except (
                    botocore.exceptions.BotoCoreError,
                    botocore.exceptions.ClientError,
                ) as e:
                    self.module.fail_json_aws(
                        e, msg="Failed to cancel resource request"
                    )

        patch = get_patch(self.module, params, properties)
        obj, error = json_patch(properties, patch)
        if error:
            self.module.fail_json(**error)
        match, diffs = diff_dicts(properties, obj)

        if not self.module.check_mode:
            # To handle idempotency when purge_* params are False (where the patch is always generated with strategy='replace')
            # call self.client.update_resource() only when there's a difference
            if diffs:
                # Wait for IN PROGRESS or PENDING resource requests to avoid concurrency exceptions
                self.wait_for_in_progress_requests(in_progress_requests, identifier)
                try:
                    response = self.client.update_resource(
                        TypeName=type_name,
                        Identifier=identifier,
                        PatchDocument=str(patch),
                        aws_retry=True,
                    )
                except (
                    botocore.exceptions.BotoCoreError,
                    botocore.exceptions.ClientError,
                ) as e:
                    self.module.fail_json_aws(e, msg="Failed to update resource")

                # Ensure the request is at least IN_PROGRESS to return updated information
                # Tag updates hangs on PENDING sometimes and updates are not reflected on the resource at this stage
                self.ensure_request_status(response)

                if self.module.params.get("wait"):
                    self.wait_until_resource_request_success(
                        response["ProgressEvent"]["RequestToken"]
                    )
            else:
                # If there's no update and wait=True
                # wait for any in_progress resource request to complete
                if self.module.params.get("wait"):
                    self.wait_for_in_progress_requests(in_progress_requests, identifier)

        results["changed"] = not match
        if self.module._diff:
            results["diff"] = diffs

        return results


class AnsibleAmazonCloudModule(AnsibleAWSModule):
    def __init__(self, **kwargs):

        super(AnsibleAmazonCloudModule, self).__init__(**kwargs)
        set_collection_info(
            collection_name=AMAZON_CLOUD_COLLECTION_NAME,
            collection_version=AMAZON_CLOUD_COLLECTION_VERSION,
        )
